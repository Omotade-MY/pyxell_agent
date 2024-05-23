import { Alert } from "@material-tailwind/react";
import { color } from "@material-tailwind/react/types/components/alert";
import { useEffect, useState } from "react";

export interface AlertUserType {
    color: color;
    message: string;
}

const AlertUser: React.FC<AlertUserType> = ({ color, message }) => {
    const [isVisible, setIsVisible] = useState(false);

    useEffect(() => {
        if (message) {
            setIsVisible(true);
            setTimeout(() => {
                setIsVisible(false);
            }, 5000);
        }
    }, [message]);

    return (
        isVisible && (
            <div className="flex w-full flex-col gap-2">
                <Alert color={color}>{message}</Alert> {/* Use state for message */}
            </div>
        )
    );
}

export default AlertUser;