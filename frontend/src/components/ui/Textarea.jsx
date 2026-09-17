import React from 'react';

const Textarea = ({
  label,
  placeholder = '',
  value = '',
  onChange,
  rows = 4,
  disabled = false,
  error = '',
  className = '',
  ...props
}) => {
  const baseStyles = 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-y bg-white';

  const errorStyles = error ? 'border-red-500 focus:ring-red-500' : '';
  const disabledStyles = disabled ? 'bg-gray-50 cursor-not-allowed opacity-50' : '';

  const classes = `
    ${baseStyles}
    ${errorStyles}
    ${disabledStyles}
    ${className}
  `.trim().replace(/\s+/g, ' ');

  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-gray-700 mb-2">
          {label}
        </label>
      )}
      <textarea
        className={classes}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        rows={rows}
        disabled={disabled}
        {...props}
      />
      {error && (
        <p className="mt-1 text-sm text-red-600">{error}</p>
      )}
    </div>
  );
};

export default Textarea;
