'use client'
import React, { MouseEvent } from 'react';

type ButtonType = "submit" | "button" | "reset" | undefined;

interface ButtonProps {
  name: string;
  type: ButtonType;
  handleSubmit: (event: MouseEvent<HTMLButtonElement>) => void;
}

const Button: React.FC<ButtonProps> = ({ name, type, handleSubmit }) => {
  return (
    <button
      type={type}
      onClick={(e) => handleSubmit(e)}
      className="w-full bg-purple-700 hover:bg-purple-900 text-white font-bold py-2 px-4 sm:px-8 sm:py-3 rounded-lg"
    >
      {name}
    </button>
  );
};

export default Button;
