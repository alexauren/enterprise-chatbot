import React, { useState } from 'react';
import styles from './about.module.css'; // Import the CSS module for styling

// Define the tabs and their corresponding content
interface Tab {
  id: number;
  title: string;
  content: string;
}
const concept = "Floyd is supposed to be a proof-of-concept showcasing the possibilites about how entreprise data and gpt models can be combines, in order to create a more intutitve way for customers to get answers to their questions. This is displayed by Microsoft in their demo which we have used and tinkered with in order to give you: 'Floyd'"

const floydInfo = `Floyd: Transforming Customer Conversations with DNB Insurance Data \n

Floyd is an innovative chat bot solution that leverages DNB-specific insurance information to revolutionize customer interactions. By harnessing the power of artificial intelligence and DNB's extensive insurance data, Floyd offers a seamless and accessible conversational experience for customers.

Using the advanced capabilities of ChatGPT and Azure Cognitive Search, Floyd understands customer inquiries and retrieves accurate, real-time insurance information from DNB's data sources. By integrating DNB-specific insurance data, Floyd provides personalized responses, helping customers make informed decisions and navigate insurance-related queries effortlessly.

Floyd's unique approach streamlines customer experiences by automating information retrieval and simplifying insurance processes. With easy access to DNB's insurance knowledge base, customers can obtain timely information, explore insurance policies, and receive tailored recommendations. Floyd empowers customers to make confident choices and enhances their overall insurance journey.

In summary, Floyd transforms customer conversations by utilizing DNB-specific insurance data. By leveraging AI capabilities, Floyd delivers personalized insights and simplifies insurance interactions, making it easier for customers to access the information they need. With Floyd, DNB enhances its commitment to exceptional customer service and provides a seamless experience within the insurance industry.`;

const TmT = "TMT is the team behind Floyd and consists of 4 summer interns. The team wants to showcase some of the possibilites with AI and how LLMs and more specifig gpt models can be used for more specific tasks"

const legalStuff = `    MIT License

Copyright (c) Microsoft Corporation.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE`

const tabs: Tab[] = [
  { id: 1, title: 'Concept', content: concept },
  { id: 2, title: 'About Floyd', content: floydInfo },
  { id: 3, title: 'About TMT', content: TmT },
  { id: 4, title: 'Legal stuff', content: legalStuff },
];

const About: React.FC = () => {
  const [activeTab, setActiveTab] = useState<Tab>(tabs[0]);

  const handleTabClick = (tab: Tab) => {
    setActiveTab(tab);
  };

  return (
    <div className={styles['about-us-page']}>
      <div className={styles.navbar}>
        {tabs.map((tab) => (
          <div
            key={tab.id}
            className={`${styles.tab} ${tab.id === activeTab.id ? styles.active : ''}`}
            onClick={() => handleTabClick(tab)}
          >
            {tab.title}
          </div>
        ))}
      </div>
      <div className={styles.content}>
        <h2 className={styles.title}>{activeTab.title}</h2>
        <p>{activeTab.content}</p>
      </div>
    </div>
  );
};

export default About;
