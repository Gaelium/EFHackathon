import React, { useEffect } from 'react'

const FilesSidebar = ({ files }) => {     

  return (
    <div className="flex flex-col bg-white w-64 p-2 mx-6 shadow-lg rounded-md h-full">
        <h1 className="text-lg font-semibold p-4 text-slate-500">All Files ({files.length})</h1>
        {files.map((file) => (
            <div className="flex flex-col px-4 py-3 mb-2 space-x-2 bg-gray-100 cursor-default rounded-md">
              <div className="text-sm font-semibold pb-1">{file.name}</div>
              <div className="text-sm italic text-gray-500">size: {(file.size / 1000000).toFixed(2)} MB</div>
            </div>
        ))}
    </div>
  )
}

export default FilesSidebar