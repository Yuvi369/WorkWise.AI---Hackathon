// src/components/auth/LoginForm.jsx
import { useState, useEffect } from 'react';

function LoginForm() {
    const [formData, setFormData] = useState({ email: '', password: '' });
    const [showPassword, setShowPassword] = useState(false);
    const [isLoaded, setIsLoaded] = useState(false);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [clickedField, setClickedField] = useState('');

    useEffect(() => {
        setTimeout(() => setIsLoaded(true), 100);
    }, []);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        setIsSubmitting(true);
        setTimeout(() => {
            setIsSubmitting(false);
            console.log('Login submitted:', formData);
        }, 2000);
    };

    const handleForgotPassword = () => {
        console.log('Forgot password clicked');
    };

    const handleSignUp = () => {
        console.log('Sign up clicked');
    };

    const handleFieldClick = (field) => {
        setClickedField(field);
        setTimeout(() => setClickedField(''), 200);
    };

    return (
        <div className={`max-w-md w-full space-y-8 transition-all duration-500`}>
            <div className={`bg-white rounded-xl shadow-lg p-8 transform transition-all duration-700 ease-out ${
                isLoaded ? 'translate-y-0 opacity-100' : '-translate-y-20 opacity-0'
            }`}>
                <div className="text-center mb-6">
                    <h2 className="text-2xl font-bold text-gray-900">Welcome Back</h2>
                    <p className="text-sm text-gray-500 mt-1">Login to your account</p>
                </div>

                <form className="space-y-6" onSubmit={handleSubmit}>
                    <div>
                        <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">Email</label>
                        <input
                            id="email"
                            name="email"
                            type="email"
                            required
                            value={formData.email}
                            onChange={handleChange}
                            onClick={() => handleFieldClick('email')}
                            placeholder="your@email.com"
                            className={`w-full px-3 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent placeholder-gray-400 bg-blue-50 transition-all duration-300 ${
                                clickedField === 'email' ? 'border-blue-500' : 'border-gray-300'
                            }`}
                        />
                    </div>

                    <div>
                        <div className="flex items-center justify-between mb-2">
                            <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                                Password
                            </label>
                            <button
                                type="button"
                                onClick={handleForgotPassword}
                                className="text-sm text-blue-600 hover:text-blue-500 transition duration-200 hover:scale-105"
                            >
                                (forgot password?)
                            </button>
                        </div>
                        <div className="relative">
                            <input
                                id="password"
                                name="password"
                                type={showPassword ? 'text' : 'password'}
                                required
                                value={formData.password}
                                onChange={handleChange}
                                onClick={() => handleFieldClick('password')}
                                placeholder="••••••••••"
                                className={`w-full px-3 py-3 pr-10 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent placeholder-gray-400 bg-blue-50 transition duration-300 ${
                                    clickedField === 'password' ? 'border-blue-500' : 'border-gray-300'
                                }`}
                            />
                            <button
                                type="button"
                                onClick={() => setShowPassword(!showPassword)}
                                className="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-500 hover:text-gray-700 transition hover:scale-110"
                            >
                                {showPassword ? (
                                    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                                            d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7
                                            a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243
                                            M9.878 9.878l4.242 4.242M9.878 9.878L8.464 8.464
                                            M9.878 9.878a3 3 0 00.007 4.243m4.242-4.242L16.536 7.464
                                            M14.12 14.12l-4.242-4.242" />
                                    </svg>
                                ) : (
                                    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                                            d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                                            d="M2.458 12C3.732 7.943 7.523 5 12 5
                                            c4.478 0 8.268 2.943 9.542 7
                                            -1.274 4.057-5.064 7-9.542 7
                                            -4.477 0-8.268-2.943-9.542-7z" />
                                    </svg>
                                )}
                            </button>
                        </div>
                    </div>

                    <div>
                        <button
                            type="submit"
                            disabled={isSubmitting}
                            className={`w-full flex justify-center items-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-gray-800 hover:bg-gray-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition-all transform ${
                                isSubmitting
                                    ? 'scale-95 opacity-80 cursor-not-allowed'
                                    : 'hover:scale-105 hover:shadow-lg active:scale-95'
                            }`}
                        >
                            {isSubmitting ? (
                                <>
                                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                                    Signing in...
                                </>
                            ) : (
                                'Sign in'
                            )}
                        </button>
                    </div>

                    <div className="text-center">
                        <p className="text-sm text-gray-600">
                            No account yet?{' '}
                            <a
                                href="/signup"
                                className="font-medium text-blue-600 hover:text-blue-500 transition transform hover:scale-105"
                            >
                                Sign up
                            </a>
                        </p>
                    </div>
                </form>
            </div>
        </div>
    );
}

export default LoginForm;
