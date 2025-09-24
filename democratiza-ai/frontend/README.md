# Democratiza AI - Frontend Documentation

## Overview

The frontend of the Democratiza AI platform is built using Next.js and React, providing a seamless user experience for contract management and legal understanding. This documentation outlines the structure, setup, and usage of the frontend application.

## Project Structure

The frontend project is organized as follows:

```
frontend
├── app                     # Main application directory
│   ├── (auth)             # Authentication routes
│   │   ├── login          # Login page
│   │   └── register       # Registration page
│   ├── (dashboard)        # Protected dashboard routes
│   │   ├── dashboard      # Dashboard page
│   │   ├── contracts      # Contracts management page
│   │   └── layout.tsx     # Dashboard layout
│   ├── layout.tsx         # Main layout for the application
│   ├── page.tsx           # Entry point for the application
│   └── globals.css        # Global styles
├── components              # Reusable components
│   ├── ui                 # UI components (buttons, cards, inputs)
│   └── features           # Feature-specific components (scanner, upload, chat)
├── lib                    # Library for API and utilities
│   ├── api.ts             # API client layer
│   └── utils.ts           # Utility functions
├── package.json           # NPM configuration
├── next.config.js         # Next.js configuration
├── tailwind.config.js      # Tailwind CSS configuration
├── tsconfig.json          # TypeScript configuration
└── README.md              # Frontend documentation
```

## Getting Started

### Prerequisites

- Node.js (version 14 or higher)
- npm (Node Package Manager)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-repo/democratiza-ai.git
   cd democratiza-ai/frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

### Running the Application

To start the development server, run:
```
npm run dev
```
The application will be available at `http://localhost:3000`.

### Building for Production

To create an optimized production build, run:
```
npm run build
```

### Testing

To run tests, use:
```
npm test
```

## Contributing

Contributions are welcome! Please follow the standard Git workflow for submitting pull requests.

## License

This project is licensed under the MIT License. See the LICENSE file for details.