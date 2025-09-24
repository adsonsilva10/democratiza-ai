import React from 'react';
import { useEffect, useState } from 'react';
import { fetchContracts } from '../../../lib/api';

const ContractsPage = () => {
    const [contracts, setContracts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const loadContracts = async () => {
            try {
                const data = await fetchContracts();
                setContracts(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        loadContracts();
    }, []);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }

    return (
        <div>
            <h1>Contracts</h1>
            <ul>
                {contracts.map(contract => (
                    <li key={contract.id}>{contract.title}</li>
                ))}
            </ul>
        </div>
    );
};

export default ContractsPage;