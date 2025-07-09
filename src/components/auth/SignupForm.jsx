import { useState, useEffect } from 'react';

function SignupForm() {
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        password: ''
    });
    const [showPassword, setShowPassword] = useState(false);
    const [isLoaded, setIsLoaded] = useState(false);
    const [clickedField, setClickedField] = useState('');

    useEffect(() => {
        setTimeout(() => setIsLoaded(true), 100);
    }, []);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log('Signup submitted:', formData);
    };

    const handleFieldClick = (fieldName) => {
        setClickedField(fieldName);
        setTimeout(() => setClickedField(''), 200);
    };

    return (
        <div className={`max-w-md w-full space-y-8`}>
            <div className={`bg-white rounded-xl shadow-lg p-8 transform transition-all duration-700 ease-out ${
                isLoaded ? 'translate-y-0 opacity-100' : '-translate-y-20 opacity-0'
            }`}>
                <div className="text-center mb-6">
                    <h2 className="text-2xl font-bold text-gray-900">Create new account</h2>
                    <p className="text-sm text-gray-500">Start your journey with us</p>
                </div>

                <form className="space-y-6" onSubmit={handleSubmit}>
                    {/* Name */}
                    <div>
                        <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">Name</label>
                        <input
                            id="name"
                            name="name"
                            type="text"
                            value={formData.name}
                            onChange={handleChange}
                            onClick={() => handleFieldClick('name')}
                            placeholder="Jane Doe"
                            required
                            className={`w-full px-3 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent placeholder-gray-400 transition-all duration-300 ease-in-out ${
                                clickedField === 'name' ? 'border-blue-500' : 'border-gray-300'
                            }`}
                        />
                    </div>

                    {/* Email */}
                    <div>
                        <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                        <input
                            id="email"
                            name="email"
                            type="email"
                            value={formData.email}
                            onChange={handleChange}
                            onClick={() => handleFieldClick('email')}
                            placeholder="you@example.com"
                            required
                            className={`w-full px-3 py-3 border rounded-lg bg-blue-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent placeholder-gray-400 transition-all duration-300 ease-in-out ${
                                clickedField === 'email' ? 'border-blue-500' : 'border-gray-300'
                            }`}
                        />
                    </div>

                    {/* Password */}
                    <div>
                        <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">Password</label>
                        <div className="relative">
                            <input
                                id="password"
                                name="password"
                                type={showPassword ? "text" : "password"}
                                value={formData.password}
                                onChange={handleChange}
                                onClick={() => handleFieldClick('password')}
                                placeholder="••••••••"
                                required
                                className={`w-full px-3 py-3 pr-10 border rounded-lg bg-blue-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent placeholder-gray-400 transition-all duration-300 ease-in-out ${
                                    clickedField === 'password' ? 'border-blue-500' : 'border-gray-300'
                                }`}
                            />
                            <button
                                type="button"
                                onClick={() => setShowPassword(!showPassword)}
                                className="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-500 hover:text-gray-700 transition-all duration-200 ease-in-out transform hover:scale-110"
                            >
                                {showPassword ? (
                                    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243" />
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.878 9.878l4.242 4.242" />
                                    </svg>
                                ) : (
                                    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                                    </svg>
                                )}
                            </button>
                        </div>
                    </div>

                    {/* Submit */}
                    <button
                        type="submit"
                        className="w-full py-3 px-4 rounded-lg text-white font-medium bg-gray-800 hover:bg-gray-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition-all duration-300 ease-in-out transform hover:scale-105 hover:shadow-lg active:scale-95"
                    >
                        Create Account
                    </button>

                    {/* Bottom link */}
                    <div className="text-center">
                        <p className="text-sm text-gray-600">
                            Already have an account?{' '}
                            <a href="/login" className="font-medium text-blue-600 hover:text-blue-500 transition-all duration-200 ease-in-out transform hover:scale-105">
                                Sign in
                            </a>
                        </p>
                    </div>
                </form>
            </div>
        </div>
    );
}

export default SignupForm;
