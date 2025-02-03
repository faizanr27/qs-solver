import React, { useState } from "react";
import "./App.css";
import { Brain, FileQuestion, Zap, CheckCircle, ArrowRight, Github, Upload } from 'lucide-react';

const FileUpload = ({ onFileUpload }) => {
  const handleChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      onFileUpload(file);
    }
  };

  return (
    <div className="relative">
      <label className="flex flex-col items-center justify-center w-64 h-40 border-2 border-green-400 border-dashed rounded-lg cursor-pointer bg-gray-900/50 hover:bg-gray-900/70 transition-all">
        <div className="flex flex-col items-center justify-center pt-5 pb-6">
          <Upload className="w-10 h-10 mb-3 text-green-400" />
          <p className="mb-2 text-sm text-gray-300">
            <span className="font-semibold">Click to upload</span> or drag and drop
          </p>
          <p className="text-xs text-gray-400">PDF, DOC, JPG or DOCX (MAX. 10MB)</p>
        </div>
        <input 
          type="file" 
          className="hidden" 
          accept=".pdf,.doc,.docx"
          onChange={handleChange}
          maxSize={10485760} // 10MB
        />
      </label>
    </div>
  );
};

const SolutionDownload = ({ isLoading, solution }) => {
  if (isLoading) {
    return (
      <div className="text-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-green-400 mx-auto"></div>
        <p className="mt-4 text-gray-300">Processing your question paper...</p>
      </div>
    );
  }

  if (solution) {
    return (
      <div className="text-center">
        <a
          href={solution}
          className="inline-flex items-center px-6 py-3 bg-green-500 text-black rounded-full font-semibold hover:bg-green-400 transition-colors gap-2"
          target="_blank"
          rel="noopener noreferrer"
        >
          Download Solution <ArrowRight className="w-4 h-4" />
        </a>
      </div>
    );
  }

  return null;
};

const App = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [solution, setSolution] = useState(null);
  const [fileName, setFileName] = useState("");

  const handleFileUpload = async (file) => {
    console.log("Uploaded file:", file);
    setFileName(file.name);
    setIsLoading(true);
    setSolution(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        setSolution(`http://localhost:5000${data.pdf_download_url}`);
      } else {
        console.error("Error:", data.error);
        setSolution(null);
      }
    } catch (error) {
      console.error("Error uploading file:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-green-500/20 to-gray-900/50 z-0" />
        {/* Animated Blobs */}
        <div className="blob blob-1" />
        <div className="blob blob-2" />
        <div className="blob blob-3" />
        {/* Content */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-32 relative z-10">
          <div className="text-center fade-in">
            <Brain className="w-16 h-16 mx-auto text-green-400 mb-8" />
            <h1 className="text-4xl sm:text-6xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-green-400 to-emerald-600">
              AI Question Paper Solver
            </h1>
            <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
              Get instant solutions and explanations for your academic questions using advanced AI technology.
            </p>
            
          </div>
        </div>
      </div>

      {/* Main Content with File Upload */}
      <div className="relative w-full flex items-center justify-center px-4">
  <div className="absolute inset-0 bg-gradient-to-b from-gray-900 to-black" />
  <div className="relative z-10 w-full max-w-3xl mx-auto text-center px-6 py-24">
    <h1 className="text-5xl font-bold mb-12 bg-clip-text text-transparent bg-gradient-to-r from-green-400 to-emerald-600">
      Upload Question Paper
    </h1>

    {/* Enlarged FileUpload */}
    <div className="flex flex-col items-center w-full">
      <FileUpload onFileUpload={handleFileUpload} className="w-full max-w-lg p-6 border border-gray-600 rounded-lg bg-gray-800/50 hover:bg-gray-800 transition-all" />
    </div>

    {/* Uploaded File Display */}
    {fileName && (
      <div className="mt-8 p-6 rounded-lg bg-green-400/10 border border-green-400/20 max-w-lg mx-auto">
        <p className="text-green-400 flex items-center justify-center gap-2 text-xl">
          <CheckCircle className="w-6 h-6" />
          Uploaded: {fileName}
        </p>
      </div>
    )}

    {/* Solution Download Section */}
    <div className="mt-12">
      <SolutionDownload isLoading={isLoading} solution={solution} />
    </div>
  </div>
</div>


      {/* Features Section */}
      <div className="py-24 bg-gray-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 ">
          <div className="grid md:grid-cols-3 gap-8 ">
            {[
              {
                icon: <FileQuestion className="w-8 h-8 text-green-400 " />,
                title: "Smart Analysis",
                description: "Our AI analyzes questions and provides detailed step-by-step solutions."
              },
              {
                icon: <Zap className="w-8 h-8 text-green-400" />,
                title: "Instant Results",
                description: "Get immediate answers and explanations for your questions."
              },
              {
                icon: <CheckCircle className="w-8 h-8 text-green-400" />,
                title: "Accurate Solutions",
                description: "High-precision answers verified by advanced AI algorithms."
              }
            ].map((feature, index) => (
              <div 
                key={index}
                className="  bg-green-400/10 border border-green-400/20 glass p-8 rounded-2xl slide-up hover-scale"
                style={{ animationDelay: `${index * 0.2}s` }}
              >
                {feature.icon}
                <h3 className="text-xl font-semibold mt-4 mb-2 text-green-400">{feature.title}</h3>
                <p className="text-gray-400">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

     
     

      {/* Footer */}
      <footer className="border-t border-gray-800 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row justify-between items-center">
          <p className="text-gray-500">© Made By Tusar Manna.</p>
          <div className="flex items-center gap-4 mt-4 sm:mt-0">
            <a href="#" className="text-gray-400 hover:text-green-400 transition-colors">
              <Github className="w-6 h-6" />
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;