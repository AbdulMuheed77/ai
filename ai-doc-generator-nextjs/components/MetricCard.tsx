import React from 'react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

interface MetricCardProps {
    title: string;
    value: string | number;
    description?: string;
    interpretation?: string;
    score?: number; // 0-100 for color coding
    icon?: React.ReactNode;
    className?: string;
}

export default function MetricCard({
    title,
    value,
    description,
    interpretation,
    score,
    icon,
    className
}: MetricCardProps) {

    // Determine badge color based on score or interpretation
    let badgeColor = 'bg-gray-100 text-gray-800';
    if (score !== undefined) {
        if (score >= 80) badgeColor = 'bg-green-100 text-green-800';
        else if (score >= 60) badgeColor = 'bg-blue-100 text-blue-800';
        else if (score >= 40) badgeColor = 'bg-yellow-100 text-yellow-800';
        else badgeColor = 'bg-red-100 text-red-800';
    }

    return (
        <div className={twMerge("bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border-l-4 border-indigo-500 hover:shadow-lg transition-shadow duration-200", className)}>
            <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider">{title}</h3>
                {icon && <span className="text-indigo-500">{icon}</span>}
            </div>

            <p className="text-3xl font-bold text-indigo-600 dark:text-indigo-400">{value}</p>

            {description && (
                <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">{description}</p>
            )}

            {interpretation && (
                <span className={clsx("inline-block px-3 py-1 rounded-full text-xs font-semibold mt-3", badgeColor)}>
                    {interpretation}
                </span>
            )}
        </div>
    );
}
