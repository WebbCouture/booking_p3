// upload_all.js
const fs = require('fs');
const path = require('path');
const cloudinary = require('cloudinary').v2;

// Configure Cloudinary (make sure your credentials are correct)
cloudinary.config({
  cloud_name: 'dnyycqlv4',
  api_key: '681482166594981',
  api_secret: 'h3CJ1TDbL-qD8mTicBxpWa38y3g',
});

const folderPath = path.join(__dirname, 'media', 'tool_images');

fs.readdir(folderPath, (err, files) => {
  if (err) {
    return console.error('Error reading directory:', err);
  }

  files.forEach(file => {
    const filePath = path.join(folderPath, file);

    cloudinary.uploader.upload(filePath, { folder: 'tool_images' })
      .then(result => {
        console.log(`Uploaded: ${file} -> ${result.secure_url}`);
      })
      .catch(error => {
        console.error(`Error uploading ${file}:`, error);
      });
  });
});
