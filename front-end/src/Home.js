import React, { useState , useEffect } from "react";
import "./App.css";
const Home = () => {
  const [messages, setmessages] = useState([
    { text: "hi", from: "bot" },
    { text: "hello", from: "user" },
    { text: "how are you", from: "bot", link: "https://www.tinkerhub.org/" },
  ]);
  //auto scroll function
  function pageScroll() {
    window.scrollBy(0, 100); // horizontal and vertical scroll increments
  }

  useEffect(()=>{
    var objDiv = document.getElementsByClassName("main")[0];
    console.log(objDiv.scrollHeight)
    objDiv.scrollTop = objDiv.scrollHeight + objDiv.offsetHeight;
    
  } , [messages])

  function getchat() {
    if (document.getElementById("inputdata").value != "") {
      let tempMessages = [...messages];

      let userMessage = {
        text: document.getElementById("inputdata").value,
        from: "user",
      };

      tempMessages.push(userMessage);
      setmessages(tempMessages);

      const data = document.getElementById("inputdata").value;
      fetch("http://127.0.0.1:5000/message", {
        method: "POST",
        headers: {
          "content-type": "application/json",
        },
        body: JSON.stringify(userMessage),
      })
        .then((response) => {
          return response.json();
        })
        .then((responseouter) => {
          let tempMessages = [...messages];
          tempMessages.push(userMessage);
          tempMessages.push({
            text: responseouter.text,
            from: "bot",
            link: responseouter.link,
          });
          setmessages(tempMessages);
       
         
       
        });

      //clear the input after sending
      document.getElementById("inputdata").value = "";
      
      
    }
  }

  return (
    <>
      <div className="navbar">
        <h2 className="heading">SPEC BOT</h2>
      </div>

      <div className="main">
        <div className="chatcontainer">
          {messages.map((message, index) => {
            return (
              <div className="chat" key={index}>
                <div className="messge">
                  {" "}
                  {message.text}
                  <br />
                  {message.link && (
                    <a
                      href={message.link}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      {message.link}
                    </a>
                  )}
                  <div className="image">
                    <img src={message.imagelink} alt="" />
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      <div className="inputbox">
        <input id="inputdata" type="text" placeholder="Enter Message" />
        <button type="submit" onClick={getchat}>
          send
        </button>
      </div>
    </>
  );
};

export default Home;
