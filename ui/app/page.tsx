'use client'

import { useState } from 'react';
import { AiFillEye, AiFillEyeInvisible } from 'react-icons/ai';
import Button from './components/Button';
import Spinner from './components/Spinner';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useAppDispatch } from '@/lib/hooks';
import { showAlert } from '@/lib/alertSlice';


interface Credential {
    username: string;
    password: string;
    confirmPassword: string;
}

const Page = () => {
    const router = useRouter();
    const dispatch = useAppDispatch();

    const [formData, setFormData] = useState<Credential>({
        username: '',
        password: '',
        confirmPassword: '',
    });


    const [passwordVisible, setPasswordVisible] = useState(false);
    const [confirmPasswordVisible, setConfirmPasswordVisible] = useState(false);
    const [errors, setErrors] = useState<Partial<Credential>>({});
    const [loading, setLoading] = useState(false);


    const togglePasswordVisibility = () => {
        setPasswordVisible(!passwordVisible);
    };

    const toggleConfirmPasswordVisibility = () => {
        setConfirmPasswordVisible(!confirmPasswordVisible);
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
        if (formData.password !== formData.confirmPassword) {
            formErrors.confirmPassword = 'Passwords do not match';
        }
        setErrors(formErrors);
        return Object.keys(formErrors).length === 0;
    };

    const handleSubmit = async (e: React.MouseEvent<HTMLButtonElement>) => {
        e.preventDefault();
        if (validateForm()) {


            try {
                setLoading(true);
                const response = await fetch(`http://127.0.0.1:8000/register/?username=${formData.username}&password=${formData.password}&confirm_password=${formData.confirmPassword}`, {
                    method: 'POST',
                });

                if (response.ok) {
                    setLoading(false);
                    dispatch(showAlert({ color: 'green', message: 'Registration successful!' }));
                    router.push('/login');
                    response.json().then(data => console.log(data))
                } else {
                    setLoading(false);
                    dispatch(showAlert({ color: 'red', message: 'Registration failed. Please try again.' }));
                    response.json().then(data => console.log(data))
                }
            } catch (error) {
                setLoading(false);
                dispatch(showAlert({ color: 'red', message: 'Registration failed. Please try again.' }));
                console.error('Error:', error);
            }
        }
    };

    return (
        <div className="bg-gradient-to-br from-purple-700 to-pink-500 min-h-screen flex flex-col justify-center items-center">
            <div className="bg-white rounded-lg shadow-lg w-[80%] p-8 sm:w-[500px] sm:py-12 max-w-md">
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
                        <label className="block text-gray-700 font-bold mb-2">Confirm Password</label>
                        <div className="relative">
                            <input
                                className={`w-full px-4 py-2 sm:py-3 rounded-lg border ${errors.confirmPassword ? 'border-red-500' : 'border-gray-400'}`}
                                type={confirmPasswordVisible ? 'text' : 'password'}
                                name="confirmPassword"
                                value={formData.confirmPassword}
                                onChange={handleChange}
                            />
                            <span
                                className="absolute right-3 top-3 cursor-pointer"
                                onClick={toggleConfirmPasswordVisibility}
                            >
                                {confirmPasswordVisible ? <AiFillEyeInvisible /> : <AiFillEye />}
                            </span>
                        </div>
                        {errors.confirmPassword && <p className="text-red-500 text-sm mt-1">{errors.confirmPassword}</p>}
                    </div>

                    <div>
                        <Button type='submit' value={!loading ? 'Register' : <Spinner />} handleSubmit={handleSubmit} />
                    </div>
                </form>
                <p className="mt-8 text-center">Have an account? <Link className="font-bold" href="/login">Sign in</Link></p>
            </div>
        </div>
    );
};

export default Page;
