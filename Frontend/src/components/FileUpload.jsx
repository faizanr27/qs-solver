import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";

const FileUpload = ({ onFileUpload }) => {
  const [file, setFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [message, setMessage] = useState("");
  const [pdfUrl, setPdfUrl] = useState(null); // Store PDF download link

  const onDrop = useCallback((acceptedFiles) => {
    setFile(acceptedFiles[0]);
    setMessage(""); 
    setPdfUrl(null);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: ".pdf,.jpg,.png,.txt,.doc,.docx",
    multiple: false,
  });

  const handleUpload = async () => {
    if (!file) {
      setMessage("⚠️ Please select a file first.");
      return;
    }

    setIsUploading(true);
    setMessage("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        setMessage("✅ File processed successfully!");
        setPdfUrl(`http://localhost:5000${data.pdf_download_url}`);
        onFileUpload(file);
      } else {
        setMessage(`❌ Error: ${data.error}`);
      }
    } catch (error) {
      console.error("Upload error:", error);
      setMessage("⚠️ Failed to upload file.");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="w-full max-w-md p-6 border-2 border-dashed border-gray-400 rounded-lg cursor-pointer bg-gray-800 hover:bg-gray-700 transition text-white text-center">
      {/* Dropzone Area */}
      <div {...getRootProps()} className="p-4">
        <input {...getInputProps()} />
        {isDragActive ? (
          <p className="text-gray-300">Drop the file here...</p>
        ) : (
          <p className="text-gray-300">Drag & drop a file here, or click to select one</p>
        )}
      </div>

      {/* Display Selected File */}
      {file && <p className="mt-4 text-gray-300">📄 {file.name}</p>}

      {/* Upload Button */}
      <button
        onClick={handleUpload}
        disabled={isUploading}
        className={`mt-4 px-4 py-2 rounded-lg transition ${
          isUploading ? "bg-gray-500 cursor-not-allowed" : "bg-blue-500 hover:bg-blue-700"
        } text-white`}
      >
        {isUploading ? "Uploading..." : "Upload"}
      </button>

      {/* Status Message */}
      {message && <p className="mt-4 text-sm">{message}</p>}

      {/* PDF Download Link */}
      {pdfUrl && (
        <a
          href={pdfUrl}
          download
          className="mt-4 px-4 py-2 bg-green-500 hover:bg-green-700 rounded-md text-white transition-colors block"
        >
          Download Solution PDF
        </a>
      )}
    </div>
  );
};

export default FileUpload;
