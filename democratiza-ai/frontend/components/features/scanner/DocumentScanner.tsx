import React, { useState } from 'react';
import { useToast } from 'shadcn/ui';
import { uploadDocument } from '../../../lib/api';

const DocumentScanner = () => {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const toast = useToast();

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleUpload = async () => {
        if (!file) {
            toast({ title: 'No file selected', status: 'error' });
            return;
        }

        setLoading(true);
        try {
            await uploadDocument(file);
            toast({ title: 'Document uploaded successfully', status: 'success' });
        } catch (error) {
            toast({ title: 'Upload failed', description: error.message, status: 'error' });
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col items-center">
            <input type="file" onChange={handleFileChange} className="mb-4" />
            <button
                onClick={handleUpload}
                disabled={loading}
                className={`btn ${loading ? 'loading' : ''}`}
            >
                {loading ? 'Uploading...' : 'Upload Document'}
            </button>
        </div>
    );
};

export default DocumentScanner;