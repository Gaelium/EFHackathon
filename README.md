# Redoct
```diff
+ Get Your Company's Documents to Reply
```

### Tech Stack

| Layer  | Description |
| ------------- | ------------- |
| Frontend  | NextJS 🏹  |
| Backend  | Flask 🐍  |
| Database  | AWS 🛢️ |

## Introduction

Redoct is a *B2B* platform for making it easy for employees, teams, and businesses to *handle internal documentation and Q/A*. It integrates with Slack and accepts multiple files that go to a chatbot that can answer employees' questions.  

## Motivation

We've all had that dreading feeling: you vaguely remember a piece of documentation that could solve your current issue at work...or was it a Slack message...wait no, maybe it was from that PowerPoint last week?? It is no surprise that internal documentation is a mess: there are so many resources floating in the ether on so many platforms. Redoct hopes to solve the issue by making it incredibly easy for companies to get answers to their own problems in one place. Redoct believes that managing documentation, however, does not have to *just* be some file manager chatbot. It has the potential to revolutionize organizational knowledge management through intuitive interfaces, powerful search algorithms, and seamless integration with existing communication platforms, thereby empowering teams to access crucial information swiftly and efficiently, ultimately driving productivity and innovation across enterprises.

## How It Works
Files, either by a company or employee for said company, get uploaded to Redoct. Additonally, the company/team slack is connected by a slackbot. The slackbot is added to necessary channels and scrapes all messages into a text file. This text file and the uploaded files get sent to AWS S3, which will be stored for analysis. 
When an employee asks a question to the Redoct chatbot, it uses embeddings to search through internal data and provide a succint answer, relying on ChatGPT in some parts.  

## Demo


https://github.com/Gaelium/EFHackathon/assets/38620265/8787f2d7-9125-4316-a930-19913cc1d69d



## Running
1) npm install
2) npm run dev
3) open [http://localhost:3000](http://localhost:3000) with your browser to see the result.
3.1) note that the Flask server will be running on [http://127.0.0.1:5328](http://127.0.0.1:5328)
