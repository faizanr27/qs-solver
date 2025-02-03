import React from 'react';
import { Loader2 } from "lucide-react";

const SolutionDownload = ({ isLoading, solution }) => {
  return (
    <div className="flex flex-col items-center justify-center p-6 border border-gray-700 rounded-lg min-w-[300px] min-h-[250px]">
      <h2 className="text-2xl font-bold mb-6">Solution</h2>

      {isLoading ? (
        <div className="flex flex-col items-center gap-4">
          <Loader2 className="h-12 w-12 animate-spin" />
          <p className="text-lg">Solving your paper...</p>
        </div>
      ) : solution ? (
        <div className="flex flex-col items-center gap-4">
          <p className="text-lg">Your solution is ready!</p>
          <a 
            href={solution}
            download  // Add the download attribute here
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-md transition-colors"
          >
            Download Solution PDF
          </a>
        </div>
      ) : (
        <p className="text-gray-400">
          Upload a question paper to get started
        </p>
      )}
    </div>
  );
};

export default SolutionDownload;