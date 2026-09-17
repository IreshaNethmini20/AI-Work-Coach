import React from 'react';

const Card = ({
  children,
  className = '',
  padding = 'md',
  ...props
}) => {
  const baseStyles = 'bg-white rounded-lg border border-gray-200 shadow-sm';

  const paddings = {
    none: '',
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8',
    xl: 'p-10'
  };

  const classes = `
    ${baseStyles}
    ${paddings[padding]}
    ${className}
  `.trim().replace(/\s+/g, ' ');

  return (
    <div className={classes} {...props}>
      {children}
    </div>
  );
};

export default Card;
