"use client";

import { useState } from 'react';

const CreateUrlPage  = () => {
    const [longUrl, setLongUrl] = useState('');
    const [shortUrl, setShortUrl] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        const response = await fetch('http://127.0.0.1:8000/short-cut/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: longUrl }),
        });

        const data = await response.json();
        setShortUrl(data.shortUrl);
    };

    return (
        <div>
            <h1>Create a Short URL</h1>
            <form onSubmit={handleSubmit}>
                <input
                type="url"
                value={longUrl}
                onChange={(e) => setLongUrl(e.target.value)}
                placeholder="Enter your long URL"
                required
                />
                <button type="submit">Create Short URL</button>
            </form>
            {shortUrl && (
                <div>
                <p>Short URL: <a href={shortUrl}>{shortUrl}</a></p>
                </div>
            )}
        </div>
    )
}

export default CreateUrlPage;