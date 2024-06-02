import React, { useState } from 'react';
import '../styles/WallpaperGenerator.css';

function WallpaperGenerator() {
  const [mainCategory, setMainCategory] = useState('');
  const [subCategory, setSubCategory] = useState('');
  const [style, setStyle] = useState('');
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);

    try {
      const response = await fetch(process.env.REACT_APP_API_URL + '/generate-wallpaper/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          main_category: mainCategory,
          sub_category: subCategory,
          style: style,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to generate wallpaper');
      }

      const imageUrl = URL.createObjectURL(await response.blob());
      setImage(imageUrl);
    } catch (error) {
      console.error('Error generating wallpaper:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Generate Wallpaper</h1>
      <form onSubmit={handleSubmit} className="form">
        <label>
          Main Category:
          <input
            type="text"
            value={mainCategory}
            onChange={(e) => setMainCategory(e.target.value)}
            required
          />
        </label>
        <label>
          Sub Category:
          <input
            type="text"
            value={subCategory}
            onChange={(e) => setSubCategory(e.target.value)}
            required
          />
        </label>
        <label>
          Style:
          <input
            type="text"
            value={style}
            onChange={(e) => setStyle(e.target.value)}
            required
          />
        </label>
        <button type="submit" disabled={loading}>
          {loading ? 'Generating...' : 'Generate Wallpaper'}
        </button>
      </form>
      {image && (
        <div className="image-container">
          <h2>Generated Wallpaper:</h2>
          <img src={image} alt="Generated Wallpaper" />
        </div>
      )}
    </div>
  );
}

export default WallpaperGenerator;
