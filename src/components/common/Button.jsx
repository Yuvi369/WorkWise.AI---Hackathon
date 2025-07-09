function Button({ children, className, type = 'button', ...props }) {
    return (
        <button
            type={type}
            className={`px-4 py-2 text-white rounded ${className}`}
            {...props}
        >
            {children}
        </button>
    );
}

export default Button;