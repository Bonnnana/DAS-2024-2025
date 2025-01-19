import React, {useState} from "react";

const AnalyseButtons = React.memo(({onButtonClick}) => {
    const [selectedDay, setSelectedDay] = useState(null);

    const handleButtonClick = (timeframe) => {
        setSelectedDay(timeframe);
        onButtonClick(timeframe); // Notify parent about the button click
    };

    return (
        <div
            className="mx-auto w-full sm:w-3/4 md:w-1/2 flex flex-col md:flex-row md:justify-evenly md:flex-wrap mt-10">
            <button
                onClick={() => handleButtonClick(1)}
                className={`w-full sm:w-[120px] mb-2 md:mb-0 border border-black rounded-2xl font-medium italic ${
                    selectedDay === 1
                        ? "bg-primary text-white border-white"
                        : "hover:bg-primary hover:text-white hover:border-white"
                }`}
            >
                1 ден
            </button>
            <button
                onClick={() => handleButtonClick(7)}
                className={`w-full sm:w-[120px] mb-2 md:mb-0 border border-black rounded-2xl font-medium italic ${
                    selectedDay === 7
                        ? "bg-primary text-white border-white"
                        : "hover:bg-primary hover:text-white hover:border-white"
                }`}
            >
                1 недела
            </button>
            <button
                onClick={() => handleButtonClick(30)}
                className={`w-full sm:w-[120px] mb-2 md:mb-0 border border-black rounded-2xl font-medium italic ${
                    selectedDay === 30
                        ? "bg-primary text-white border-white"
                        : "hover:bg-primary hover:text-white hover:border-white"
                }`}
            >
                1 месец
            </button>
        </div>
    );
});

export default AnalyseButtons;
