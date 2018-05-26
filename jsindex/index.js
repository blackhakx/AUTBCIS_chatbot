'use strict';
 
const functions = require('firebase-functions');
const {WebhookClient} = require('dialogflow-fulfillment');
const {Card, Suggestion} = require('dialogflow-fulfillment');

process.env.DEBUG = 'dialogflow:debug'; // enables lib debugging statements

//JSON texts to objects
const mathReq = '{"Analytics": "STAT500 Applied Statistics or MATH501 Differential & Integral Calculus",' +
    '"ComputationalIntelligence": "STAT500 Applied Statistics",' +
    '"ComputerScience": "MATH502 Algebra & Discrete Mathematics",' + 
    '"ITServiceSciences": "STAT500 Applied Statistics or MATH500 Mathematical Concepts or MATH501 Differential & Integral Calculus or MATH502 Algebra & Discrete Mathematics",' +
    '"NetworkSecurity": "STAT500 Applied Statistics or MATH500 Mathematical Concepts or MATH501 Differential & Integral Calculus or MATH502 Algebra & Discrete Mathematics",' +
    '"SoftwareDevelopment": "STAT500 Applied Statistics or MATH500 Mathematical Concepts or MATH501 Differential & Integral Calculus or MATH502 Algebra & Discrete Mathematics"}';

const mathReqObj = JSON.parse(mathReq);

const preReq = '{"Programming2": "Programming 1",' +
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

const preReqObj = JSON.parse(preReq);

const coReq = '{"ProgrammingDesignConstruction": "IT Project Management",' +
    '"SoftwareDevelopmentPractice": "Data & Process Modelling"}';

const coReqObj = JSON.parse(coReq);

const majorPapers = '{"SoftwareDevelopment": "COMP603, COMP602, COMP604, INFS602, ENSE701, COMP719, COMP721, COMP713",'+
    '"ComputerScience": "COMP610, COMP611, COMP604, COMP613, COMP711, COMP712, COMP717, COMP713",'+
    '"ITServiceScience": "COMP601, INFS603, COMP609, COMP607, INFS701, INFS702, COMP718, INFS703",'+
    '"NetworksSecurity": "ENEL611, COMP609, COMP604, INFS602, COMP714, COMP715, COMP718, COMP713", '+
    '"ComputationalIntelligence": "COMP606, STAT601, COMP610, INFS602, COMP717, COMP723, COMP700, COMP701", '+
    '"Analytics": "STAT600, STAT601, STAT603, STAT702, STAT700, COMP723, STAT701" }';

const majorPapersObj = JSON.parse(majorPapers);

const job = '{"ComputerProgrammer": "Software Development",'+
    '"MobileAppDeveloper": "Software Development",' + 
    '"SoftwareDeveloper": "Software Development",' +
    '"SoftwareEngineer": "Software Development",' +
    '"SoftwareTester": "Software Development",' +
    '"SystemsAnalyst": "Software Development",' +
    '"SystemsArchitect": "Software Development or Computer Science",' +
    '"TechonlogyConsultant": "Software Development",' +
    '"WebDeveloper": "Software Development",' + 
    '"ProjectManager": "Software Development",' +
    '"Biostician": "Analytics",' + 
    '"BusinessAnalyst": "Analytics",' +
    '"GovernmentStatistician": "Analytics",' +
    '"IndustrialForecaster": "Analytics",' +
    '"LogisticsAnalyst": "Analytics or Computational Intelligence or IT Service Science",' +
    '"SecondaryTeacher": "Analytics",' +
    '"DataAnalyst": "Computational Intelligence",' +
    '"InformationAnalyst": "Computational Intelligence",' + 
    '"ITSupervisor": "Computational Intelligence",' + 
    '"ISServicesConsultant": "Computational Intelligence",' +
    '"TechnicalAnalyst": "Computational Intelligence",' +
    '"ProjectLeader": "Computational Intelligence",' +
    '"Entrepreneur": "Computer Science",' +
    '"IndustrialResearcher": "Computer Science",' +
    '"SoftwareDesigner": "Computer Science",' +
    '"DatabaseAdministrator": "IT Service Science",' +
    '"ITSecurityAnalyst": "Networks and Security"}';

const jobObj = JSON.parse(job);

const sem = '{"AppliedCommunication": "Semester 1 in both campus and Semester 2 in both campus",' +
    '"Programming1": "Semester 1 in both campus and Semester 2 in both campus",' +
    '"ComputingTechnologinSociety": "Semester 1 in both campus and Semester 2 in both campus",' +
    '"FoundationsofITInfrastructure": "Semester 1 in both campus and Semester 2 in both campus",' +
    '"EnterpriseSystems": "Semester 1 in both campus and Semester 2 in both campus",' +
    '"Programming2": "Semester 1 in both campus and Semester 2 in both campus",' +
    '"ComputerNetworkPrinciples": "Semester 1 in both campus and Semester 2 in both campus",' +
    '"AppliedStatistics": "Semester 1 in City campus and Semester 2 in both campus",' +
    '"DifferentialIntegralCalculus": "Semester 2 in City campus",' +
    '"AlgebraDiseteMathematics": "Semester 1 in City campus and Semester 2 in both campus",' +
    '"MathematicalConcepts": "Semester 1 in both campus and Semester 2 in both campus",' +
    '"DataProcessingModelling": "Semester 1 in both campus and Semester 2 in both campus",' +
    '"LogicalDatabaseDesign": "Semester 1 in both campus and Semester 2 in both campus",' +
    '"ITProjectManagement": "Semester 1 in both campus and Semester 2 in both campus",' +
    '"ProgrammingDesignConstruction": "Semester 1 in both campus and Semester 2 in both campus",' +
    '"SoftwareDevelopmentPractice": "Semester 1 in both campus and Semester 2 in both campus",' +
    '"OperatingSystems": "Semester 1 in South campus and Semester 2 in both campus",' +
    '"PhysicalDatabaseDesign": "Semester 1 in both campus and Semester 2 in both campus",' +
    '"SoftwareEngineering": "Semester 1 in both campus and Semester 2 in both campus",' +
    '"AppliedHumanComputerInteraction": "Semester 1 in both campus and Semester 2 in both campus",' +
    '"WebDevelopment": "Semester 1 in both campus",' +
    '"DistributedMobileSystems": "Semester 1 in City campus and Semester 2 in City campus"}';
    
const semObj = JSON.parse(sem);

const fail = '{"EnterpriseSystems": "Data Process & Modelling and Logical Database Design",' +
    '"Programming1": "Programming 2",' + 
    '"Programming2": "Program Design & Construction, Physical Database Design, and Operating Systems",' +
    '"FoundationsofITInfrastructure": "Operating Systems",' +
    '"ProgrammingDesignConstruction": "Software Development Practice, Software Development, and Web Development",' +
    '"LogicalDatabaseDesign": "Physical Database Design",' +
    '"SoftwareDevelopmentPractice": "Research and Development Project",' +
    '"ITProjectManagement": "Research and Development Project"}';
    
const failObj = JSON.parse(fail);
    
exports.dialogflowFirebaseFulfillment = functions.https.onRequest((request, response) => {
  const agent = new WebhookClient({ request, response });
  console.log('Dialogflow Request headers: ' + JSON.stringify(request.headers));
  console.log('Dialogflow Request body: ' + JSON.stringify(request.body));
 
  function welcome(agent) {
    agent.add(`Hi, I am your career advisor, how can I help you?`);
  }
 
  function fallback(agent) {
    agent.add(`I didn't understand`);
    agent.add(`I'm sorry, can you try again?`);
}

  //Intent functions
   function getstudy(agent) {
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
   
   function getCoreq(agent){
       const requestedPaper = agent.parameters.paper;
       console.log("entity:: " + requestedPaper);
       if (coReqObj.hasOwnProperty(requestedPaper)){
           var paperCoreq = coReqObj[requestedPaper];
           console.log("paper:: " + paperCoreq);
           var paperCoreqs = JSON.stringify(paperCoreq);
           console.log(paperCoreqs);
       agent.add(paperCoreqs);}
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
   
   function getEligibility(agent){
       const requestedPaper = agent.parameters.paper;
       console.log("entity:: " + requestedPaper);
       if (preReqObj.hasOwnProperty(requestedPaper)){
           var paperReq = preReqObj[requestedPaper];
           console.log("paper:: " + paperReq);
           var paperReqs = JSON.stringify(paperReq);
           console.log(paperReqs);
           agent.add("If you have taken these papers");
           agent.add(paperReqs);
           agent.add("Then you can apply to that paper");
       }
       else{
           agent.add("Yes, you are eligible");
       }
   }
   
   function getJob(agent){
       const requestedJob = agent.parameters.job;
       console.log("entity:: " + requestedJob);
       var course = jobObj[requestedJob];
       var courses = JSON.stringify(course);
       agent.add("You can do");
       agent.add(courses);
   }
   
   function getSem(agent){
       const requestedPaper = agent.parameters.paper;
       console.log("entity:: " + requestedPaper);
       if (semObj.hasOwnProperty(requestedPaper)){
           var paperSem = semObj[requestedPaper];
           console.log("paper:: " + paperSem);
           var paperSems = JSON.stringify(paperSem);
           console.log(paperSems);
           agent.add("It is offered in");
           agent.add(paperSems);}
       else{
           agent.add("It is not offered");
       }
   }
   
   function getFail(agent){
       const requestedPaper = agent.parameters.paper;
       console.log("entity:: " + requestedPaper);
       if (failObj.hasOwnProperty(requestedPaper)){
           var paperSem = failObj[requestedPaper];
           console.log("paper:: " + paperSem);
           var paperSems = JSON.stringify(paperSem);
           console.log(paperSems);
           agent.add("You cannot take");
           agent.add(paperSems);}
       else{
           agent.add("There is no restriction on the papers that you can take");
       }
   }

  // Run the proper function handler based on the matched Dialogflow intent name
  let intentMap = new Map();
  intentMap.set('Default Welcome Intent', welcome);
  intentMap.set('Default Fallback Intent', fallback);
  intentMap.set('study', getstudy);
  intentMap.set('pre-req', getPrereq);
  intentMap.set('math', getMath);
  intentMap.set('co-req', getCoreq);
  intentMap.set('eligiblility', getEligibility);
  intentMap.set('job', getJob);
  intentMap.set('sem', getSem);
  intentMap.set('fail', getFail);
  agent.handleRequest(intentMap);
});
