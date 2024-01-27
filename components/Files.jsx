import React from 'react'

const Files = ({ files }) => {
  return (
    <div className="flex flex-col bg-white w-64 p-2">
        <h1 className="text-lg">Files</h1>
        {files.map((file, index) => (
            <div key={index}>
                <h2>{file.name}</h2>
                <p>{file.description}</p>
            </div>
        ))}
    </div>
  )
}

export default Files