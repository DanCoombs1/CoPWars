import React from 'react';

const CustomAvatar = ({ 
  skinColor = 0, 
  hairStyle = 0, 
  hairColor = 0, 
  topStyle = 0, 
  topColor = 0, 
  size = 128 
}) => {
  // Dicebear pixel art API configuration
  const seed = `avatar-${skinColor}-${hairStyle}-${hairColor}-${topStyle}-${topColor}`;
  
  // Map our values to Dicebear options
  const skinColors = ['light', 'yellow', 'brown', 'dark', 'red', 'black'];
  const hairStyles = ['short', 'long', 'eyepatch', 'turban', 'winterHat1', 'winterHat2', 'winterHat3', 'winterHat4'];
  const hairColors = ['blonde', 'orange', 'black', 'white', 'brown', 'blue', 'pink'];
  const topStyles = ['blazerShirt', 'blazerSweater', 'collarSweater', 'graphicShirt', 'hoodie', 'overall', 'shirtCrewNeck', 'shirtScoopNeck'];
  const topColors = ['black', 'blue01', 'blue02', 'blue03', 'gray01', 'gray02', 'heather', 'pastelBlue', 'pastelGreen', 'pastelOrange', 'pastelRed', 'pastelYellow', 'pink', 'red', 'white'];

  const currentSkinColor = skinColors[skinColor % skinColors.length];
  const currentHairStyle = hairStyles[hairStyle % hairStyles.length];
  const currentHairColor = hairColors[hairColor % hairColors.length];
  const currentTopStyle = topStyles[topStyle % topStyles.length];
  const currentTopColor = topColors[topColor % topColors.length];

  // Build Dicebear URL - using a more reliable approach
  const dicebearUrl = `https://api.dicebear.com/7.x/pixel-art/svg?seed=${seed}`;

  return (
    <img 
      src={dicebearUrl}
      alt="Avatar"
      width={size}
      height={size}
      style={{ 
        borderRadius: '50%',
        border: '2px solid #ddd'
      }}
      onError={(e) => {
        console.error('Failed to load avatar:', dicebearUrl);
        e.target.style.display = 'none';
      }}
      onLoad={() => {
        console.log('Avatar loaded successfully:', dicebearUrl);
      }}
    />
  );
};

export default CustomAvatar;
