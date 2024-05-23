'use client'
import React, { useState } from 'react';
import { AiFillEye, AiFillEyeInvisible } from 'react-icons/ai';
import Button from '../components/Button'
import Spinner from '../components/Spinner';
import Link from 'next/link';
import { useRouter } from 'next/navigation';



interface Credential {
    username: string;
    password: string;
}

const Page = () => {
    const [formData, setFormData] = useState<Credential>({
        username: '',
        password: '',
    });

    const [passwordVisible, setPasswordVisible] = useState(false);
    const [errors, setErrors] = useState<Partial<Credential>>({});
    const [loading, setLoading] = useState(false);


    const togglePasswordVisibility = () => {
        setPasswordVisible(!passwordVisible);
    };

    const handleChange = (event: React.FormEvent<HTMLInputElement>) => {
        const { name, value } = event.currentTarget;
        setFormData({
            ...formData,
            [name]: value,
        });
    };

    const validateForm = () => {
        let formErrors: Partial<Credential> = {};
        if (!formData.username) formErrors.username = 'Username is required';
        if (!formData.password) formErrors.password = 'Password is required';
        setErrors(formErrors);
        return Object.keys(formErrors).length === 0;
    };

    const handleSubmit = async (e: React.MouseEvent<HTMLButtonElement>) => {
        e.preventDefault();
        if (validateForm()) {
            const data = new URLSearchParams({
                username: formData.username,
                password: formData.password,
            });
            try {
                setLoading(true);
                const response = await fetch(`http://127.0.0.1:8000/login`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: data,
                });

                if (response.ok) {
                    setLoading(false);
                    alert('Login successful!');
                    response.json().then(data => {
                        console.log(data)
                        localStorage.setItem('token', data.token)
                    }
                       
                    )
                } else {
                    setLoading(false);
                    alert('Login failed. Please try again.');
                    response.json().then(data => console.log(data))
                }
            } catch (error) {
                setLoading(false);
                console.error('Error:', error);
            }
        }
    };

    return (
        <div className="bg-gradient-to-br from-purple-700 to-pink-500 min-h-screen flex flex-col justify-center items-center">
            <div className="bg-white rounded-lg w-[80%] shadow-lg p-8 sm:w-[500px] sm:py-12 max-w-md">
                <h1 className="text-4xl font-bold text-center text-purple-700 mb-8">Pyxell AI</h1>
                <form className="space-y-6">
                    <div>
                        <label className="block text-gray-700 font-bold mb-2">Username</label>
                        <input
                            className={`w-full px-4 py-2 sm:py-3 rounded-lg border ${errors.username ? 'border-red-500' : 'border-gray-400'}`}
                            type="text"
                            name="username"
                            value={formData.username}
                            onChange={handleChange}
                        />
                        {errors.username && <p className="text-red-500 text-sm mt-1">{errors.username}</p>}
                    </div>

                    <div>
                        <label className="block text-gray-700 font-bold mb-2">Password</label>
                        <div className="relative">
                            <input
                                className={`w-full px-4 py-2 sm:py-3 rounded-lg border ${errors.password ? 'border-red-500' : 'border-gray-400'}`}
                                type={passwordVisible ? 'text' : 'password'}
                                name="password"
                                value={formData.password}
                                onChange={handleChange}
                            />
                            <span
                                className="absolute right-3 top-3 cursor-pointer"
                                onClick={togglePasswordVisibility}
                            >
                                {passwordVisible ? <AiFillEyeInvisible /> : <AiFillEye />}
                            </span>
                        </div>
                        {errors.password && <p className="text-red-500 text-sm mt-1">{errors.password}</p>}
                    </div>

                    <div>
                        <Button type='submit' value={!loading ? 'Login' : <Spinner />} handleSubmit={handleSubmit} />
                    </div>
                </form>
                <p className="mt-8 text-center">Don&apos;t have an account? <Link className="font-bold" href="/">Sign up</Link></p>
            </div>
        </div>
    );
};

export default Page;
