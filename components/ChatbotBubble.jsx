import React from 'react'
import Image from 'next/image'

const ChatbotBubble = ({ message }) => {
  return (
    <div className="flex w-full mt-2 space-x-3 max-w-xs">
        <Image src="/chatbot.png" width={100} height={100} className="flex-shrink-0 h-10 w-10 rounded-full bg-gray-200" alt="chat bot icon"/>
        <div>
            <div className="bg-gray-300 p-3 rounded-r-lg rounded-bl-lg">
                <p className="text-sm">
                    {message}
                </p>
            </div>
            {/* <span className="text-xs text-gray-500 leading-none">
                2 min ago
            </span> */}
        </div>
    </div>
  )
}

export default ChatbotBubble