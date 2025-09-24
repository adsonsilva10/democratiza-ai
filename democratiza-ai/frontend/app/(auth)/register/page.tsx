import React, { useState } from 'react';
import { useRouter } from 'next/router';
import { api } from '../../../lib/api';
import Input from '../../../components/ui/input';
import Button from '../../../components/ui/button';

const RegisterPage = () => {
    const router = useRouter();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleRegister = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            await api.post('/auth/register', { email, password });
            router.push('/auth/login');
        } catch (err) {
            setError('Registration failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen">
            <h1 className="text-2xl font-bold mb-4">Register</h1>
            {error && <p className="text-red-500">{error}</p>}
            <form onSubmit={handleRegister} className="w-full max-w-sm">
                <Input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
                <Input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
                <Button type="submit" disabled={loading}>
                    {loading ? 'Registering...' : 'Register'}
                </Button>
            </form>
            <p className="mt-4">
                Already have an account? <a href="/auth/login" className="text-blue-500">Login</a>
            </p>
        </div>
    );
};

export default RegisterPage;