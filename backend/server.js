// Import necessary packages
const express = require('express');
const axios = require('axios');
const cors = require('cors');
require('dotenv').config();

// Create an Express application
const app = express();
const PORT = process.env.PORT || 8000; // Use port 8000 by default

// --- Judge0 API Configuration ---
const JUDGE0_API_KEY = process.env.JUDGE0_API_KEY;
const JUDGE0_API_HOST = "judge0-ce.p.rapidapi.com";

if (!JUDGE0_API_KEY) {
    console.error('JUDGE0_API_KEY environment variable is required');
    process.exit(1);
}

// --- Middleware ---
// Enable Cross-Origin Resource Sharing (CORS) so your React app can talk to this server
app.use(cors());
// Enable the server to parse JSON request bodies
app.use(express.json());



// --- Helper Function to map our language names to Judge0's language IDs ---
const getLanguageId = (language) => {
    switch (language.toLowerCase()) {
        case 'python': return 92;     // Python 3
        case 'java': return 91;       // Java
        case 'c++': return 54;        // C++ (GCC)
        case 'csharp': return 51;     // C#
        case 'sql': return 82;        // SQL (SQLite)
        default: return null;
    }
};

// --- API Endpoint to Execute Code ---
app.post('/execute', async (req, res) => {
    // Get the language and code from the request body sent by the React app
    const { language, code, testCases } = req.body;

    const languageId = getLanguageId(language);
    if (languageId === null) {
        return res.status(400).json({ error: 'Unsupported language' });
    }

    // For console runs (empty test cases), we don't need input
    // For test runs, we use the first test case input
    const testInput = testCases.length > 0 ? testCases[0].input : '';
    const expectedOutput = testCases.length > 0 ? testCases[0].expectedOutput : '';
    const isConsoleRun = testCases.length === 0;

    // Wrap user code with test harness for Python
    let finalCode = code;
    if (!isConsoleRun && language === 'python' && testInput) {
        finalCode = `${code}

# Auto-generated test harness
import ast
sol = Solution()
nums = ast.literal_eval('${testInput}')
result = sol.firstMissingPositive(nums)
print(result)`;
    }

    // --- Step 1: Create a submission to Judge0 ---
    try {
        console.log('Sending code to Judge0:', {
            language,
            languageId,
            codeLength: code.length,
            testCasesLength: testCases.length,
            isConsoleRun
        });
        
        const submissionOptions = {
            method: 'POST',
            url: 'https://judge0-ce.p.rapidapi.com/submissions',
            params: {
                base64_encoded: 'true',
                wait: 'false' // We will poll for the result, so we don't wait here
            },
            headers: {
                'content-type': 'application/json',
                'X-RapidAPI-Key': JUDGE0_API_KEY,
                'X-RapidAPI-Host': JUDGE0_API_HOST
            },
            data: {
                language_id: languageId,
                // Encode the source code to Base64 to handle special characters
                source_code: Buffer.from(finalCode).toString('base64'),
                stdin: Buffer.from('').toString('base64'), // No stdin needed since test harness handles input
            }
        };

        const submissionResponse = await axios.request(submissionOptions);
        console.log('Judge0 submission response:', submissionResponse.data);
        const submissionToken = submissionResponse.data.token;

        // --- Step 2: Poll for the result using the submission token ---
        let resultResponse;
        let statusId = 1; // 1 = "In Queue"

        // Keep checking every 2 seconds until the status is no longer "In Queue" or "Processing"
        while (statusId === 1 || statusId === 2) {
            await new Promise(resolve => setTimeout(resolve, 2000)); // Wait for 2 seconds

            const resultOptions = {
                method: 'GET',
                url: `https://judge0-ce.p.rapidapi.com/submissions/${submissionToken}`,
                params: {
                    base64_encoded: 'true',
                    fields: '*'
                },
                headers: {
                    'X-RapidAPI-Key': JUDGE0_API_KEY,
                    'X-RapidAPI-Host': JUDGE0_API_HOST
                }
            };
            resultResponse = await axios.request(resultOptions);
            console.log('Judge0 polling result:', {
                statusId: resultResponse.data.status.id,
                statusDescription: resultResponse.data.status.description,
                hasStdout: !!resultResponse.data.stdout,
                hasStderr: !!resultResponse.data.stderr
            });
            statusId = resultResponse.data.status.id;
        }

        // --- Step 3: Process and send the final result back to the React app ---
        const result = resultResponse.data;
        
        // Check if the execution was successful
        if (result.status.id === 3) { // 3 = "Accepted"
            const actualOutput = Buffer.from(result.stdout, 'base64').toString().trim();
            
            if (isConsoleRun) {
                // For console runs, just return the output
                res.json({
                    status: result.status,
                    time: result.time || 0,
                    memory: result.memory || 0,
                    stdout: result.stdout,
                    stderr: result.stderr,
                    actualOutput: actualOutput
                });
            } else {
                // For test runs, check if output matches expected output
                const allTestsPassed = actualOutput === expectedOutput;
                
                res.json({
                    status: result.status,
                    time: result.time || 0,
                    memory: result.memory || 0,
                    stdout: result.stdout,
                    stderr: result.stderr,
                    allTestsPassed: allTestsPassed,
                    actualOutput: actualOutput,
                    expectedOutput: expectedOutput
                });
            }
        } else {
            // Execution failed or had errors
            let errorMessage = '';
            
            if (result.stderr) {
                errorMessage = Buffer.from(result.stderr, 'base64').toString();
            } else if (result.status.description) {
                errorMessage = result.status.description;
            } else {
                errorMessage = 'Execution failed';
            }
            
            // Add more context based on status
            switch (result.status.id) {
                case 4: // Wrong Answer
                    errorMessage = `Wrong Answer: Your output doesn't match the expected result.\n\nExpected: ${expectedOutput}\nGot: ${result.stdout ? Buffer.from(result.stdout, 'base64').toString().trim() : '(no output)'}`;
                    break;
                case 5: // Time Limit Exceeded
                    errorMessage = 'Time Limit Exceeded: Your code took too long to execute.';
                    break;
                case 6: // Compilation Error
                    errorMessage = `Compilation Error:\n${errorMessage}`;
                    break;
                case 7: // Runtime Error
                    errorMessage = `Runtime Error:\n${errorMessage}`;
                    break;
                case 8: // Memory Limit Exceeded
                    errorMessage = 'Memory Limit Exceeded: Your code used too much memory.';
                    break;
                default:
                    errorMessage = `Execution Error (Status ${result.status.id}): ${errorMessage}`;
            }
            
            res.json({
                status: result.status,
                time: result.time || 0,
                memory: result.memory || 0,
                stdout: result.stdout,
                stderr: result.stderr,
                allTestsPassed: false,
                errorMessage: errorMessage
            });
        }

    } catch (error) {
        console.error('Error with Judge0 API:', error.response ? error.response.data : error.message);
        console.error('Full error object:', error);
        
        // Send more detailed error information
        if (error.response) {
            res.status(500).json({ 
                error: `Judge0 API Error: ${error.response.status} - ${error.response.statusText}`,
                details: error.response.data
            });
        } else if (error.request) {
            res.status(500).json({ 
                error: 'No response received from Judge0 API',
                details: error.message
            });
        } else {
            res.status(500).json({ 
                error: 'Error setting up request to Judge0 API',
                details: error.message
            });
        }
    }
});


// --- Test endpoint to verify Judge0 API ---
app.get('/test-judge0', async (req, res) => {
    try {
        console.log('Testing Judge0 API connection...');
        
        const testOptions = {
            method: 'GET',
            url: 'https://judge0-ce.p.rapidapi.com/languages',
            headers: {
                'X-RapidAPI-Key': JUDGE0_API_KEY,
                'X-RapidAPI-Host': JUDGE0_API_HOST
            }
        };
        
        const response = await axios.request(testOptions);
        console.log('Judge0 API test successful:', response.data.length, 'languages available');
        res.json({ 
            success: true, 
            message: 'Judge0 API is working',
            languagesCount: response.data.length
        });
    } catch (error) {
        console.error('Judge0 API test failed:', error.response ? error.response.data : error.message);
        res.status(500).json({ 
            success: false, 
            error: 'Judge0 API test failed',
            details: error.response ? error.response.data : error.message
        });
    }
});

// --- Start the Server ---
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
