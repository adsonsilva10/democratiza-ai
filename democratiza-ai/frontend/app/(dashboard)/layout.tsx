import React from 'react';

const DashboardLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    return (
        <div className="flex flex-col h-screen">
            <header className="bg-blue-600 text-white p-4">
                <h1 className="text-xl">Dashboard</h1>
            </header>
            <main className="flex-1 p-4">
                {children}
            </main>
            <footer className="bg-gray-200 p-4 text-center">
                <p>&copy; {new Date().getFullYear()} Democratiza AI</p>
            </footer>
        </div>
    );
};

export default DashboardLayout;