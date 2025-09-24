import React, { useState } from 'react';
import { useRouter } from 'next/router';
import { api } from '../../../lib/api';
import { Input } from '../../../components/ui/input';
import { Button } from '../../../components/ui/button';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const router = useRouter();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const response = await api.post('/api/v1/auth/login', { email, password });
      // Handle successful login (e.g., store token, redirect)
      router.push('/(dashboard)/dashboard');
    } catch (err) {
      setError('Invalid email or password');
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-2xl font-bold mb-4">Login</h1>
      {error && <p className="text-red-500">{error}</p>}
      <form onSubmit={handleLogin} className="w-full max-w-sm">
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
        <Button type="submit" className="mt-4">Login</Button>
      </form>
    </div>
  );
};

export default LoginPage;