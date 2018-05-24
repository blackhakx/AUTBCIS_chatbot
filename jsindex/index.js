// See https://github.com/dialogflow/dialogflow-fulfillment-nodejs
// for Dialogflow fulfillment library docs, samples, and to report issues
'use strict';
 
const functions = require('firebase-functions');
const {WebhookClient} = require('dialogflow-fulfillment');
const {Card, Suggestion} = require('dialogflow-fulfillment');

process.env.DEBUG = 'dialogflow:debug'; // enables lib debugging statements


const mathReq = '{"Analytics": "STAT500 Applied Statistics or MATH501 Differential & Integral Calculus",' +
    '"ComputationalIntelligence": "STAT500 Applied Statistics",' +
    '"ComputerScience": "MATH502 Algebra & Discrete Mathematics",' + 
    '"ITServiceSciences": "STAT500 Applied Statistics or MATH500 Mathematical Concepts or MATH501 Differential & Integral Calculus or MATH502 Algebra & Discrete Mathematics",' +
    '"NetworkSecurity": "STAT500 Applied Statistics or MATH500 Mathematical Concepts or MATH501 Differential & Integral Calculus or MATH502 Algebra & Discrete Mathematics",' +
    '"SoftwareDevelopment": "STAT500 Applied Statistics or MATH500 Mathematical Concepts or MATH501 Differential & Integral Calculus or MATH502 Algebra & Discrete Mathematics"}';

const mathReqObj = JSON.parse(mathReq);

var preReq = '{"Programming2": "Programming 1",' +
    '"DataProcessModelling": "Programming 1",' +
    '"LogicalDatabaseDesign": "Programming 1 or Programming for Engineering Applications",' +
    '"ProgrammingDesignConstruction": "Programming 2",' + 
    '"SoftwareDevelopmentPractice": "Programming Design & Construction or Data Structures & Algorithms",' +
    '"OperatingSystems": "Foundations of IT Infrastructure and choose between Programming 2 or Data Structures & Algorithms",' +
    '"PhysicalDatabaseDesign": "Programming 2 and Logical Database Design",' +
    '"SoftwareEngineering": "Program Design & Construction or Data Structures & Algorithms",' +
    '"WebDevelopment":  "Program Design & Construction",' +
    '"DistributedMobileSystems": "Algorithm Design & Analysis",' +
    '"ResearchDevelopmentProjectPart1": "IT Project Management & Software Development Practice",' +
    '"ResearchDevelopmentProjectPart2": "ResearchDevelopmentProjectPart1"}';

var preReqObj = JSON.parse(preReq);

var coReq = '{"ProgrammingDesignConstruction": "IT Project Management",' +
    '"SoftwareDevelopmentPractice": "Data & Process Modelling"}';

var coReqObj = JSON.parse(coReq);

var majorPapers = '{"SoftwareDevelopment": "COMP603, COMP602, COMP604, INFS602, ENSE701, COMP719, COMP721, COMP713"}';

var majorPapersObj = JSON.parse(majorPapers);

 
exports.dialogflowFirebaseFulfillment = functions.https.onRequest((request, response) => {
  const agent = new WebhookClient({ request, response });
  console.log('Dialogflow Request headers: ' + JSON.stringify(request.headers));
  console.log('Dialogflow Request body: ' + JSON.stringify(request.body));
  
  function welcome(agent) {
    agent.add(`Welcome to my agent!`);
  }
 
  function fallback(agent) {
    agent.add(`I didn't understand`);
    agent.add(`I'm sorry, can you try again?`);
  }


  // // Uncomment and edit to make your own intent handler
  // // uncomment `intentMap.set('your intent name here', yourFunctionHandler);`
  // // below to get this function to be run when a Dialogflow intent is matched
  
   function getstudy(agent) {
       //var parameters = request.body.queryResult.parameters.major;
       /*
       var reply = "study";
       var major = "SoftwareDevelopment";
       var majorPapers = majorPapersObj[major];
       console.log("study");
              //console.log("This is the reply " + reply);
       agent.add("this is trial respons " + reply);
       agent.add(majorPapers)
       */
       const requestedMajor = agent.parameters.major;
       console.log("entity:: " + requestedMajor);
       if (majorPapersObj.hasOwnProperty(requestedMajor)){
           var majorPaper = majorPapersObj[requestedMajor];
           console.log("papers:: " + majorPaper);
           var majorPapers = JSON.stringify(majorPaper);
           console.log(majorPapers);
           agent.add("Here are the major papers:")
           agent.add(majorPapers);}
       else{
           agent.add("We don't offer that paper");
       }
   }

    function getPrereq(agent){
       const requestedPaper = agent.parameters.paper;
       console.log("entity:: " + requestedPaper);
       if (preReqObj.hasOwnProperty(requestedPaper)){
           var paperReq = preReqObj[requestedPaper];
           console.log("paper:: " + paperReq);
           var paperReqs = JSON.stringify(paperReq);
           console.log(paperReqs);
       agent.add(paperReqs);}
       else{
           agent.add("None");
       }
   }
   
   function getMath(agent){
       const requestedMajor = agent.parameters.major;
       console.log("entity:: " + requestedMajor);
       var mathPaper = mathReqObj[requestedMajor];
       var mathPapers = JSON.stringify(mathPaper);
       agent.add("Math papers that you can take are: ");
       agent.add(mathPapers);
   }

  // Run the proper function handler based on the matched Dialogflow intent name
  let intentMap = new Map();
  intentMap.set('Default Welcome Intent', welcome);
  intentMap.set('Default Fallback Intent', fallback);
  intentMap.set('study', getstudy);
  intentMap.set('pre-req', getPrereq);
  intentMap.set('math', getMath);
  // intentMap.set('your intent name here', googleAssistantHandler);
  agent.handleRequest(intentMap);
});