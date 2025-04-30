@RestResource(urlMapping='/api/Slack/*')
global with sharing class AgentInvokeProdRecoandDiscModel {

   @HttpPost
   global static String invokeJavaAction() {
       try {
         
           // Create an instance of the invocable action with type ‘generateAiAgentResponse’ and name ‘Agentforce_Service_Agent_new’
           Invocable.Action action = Invocable.Action.createCustomAction('generateAiAgentResponse', 'Agentforce_Service_Agent_PR');
          
           action.setInvocationParameter('userMessage', 'Please create Quote for me for a Mobile with gaming usages');
           
          
           // Execute the action
           List<Invocable.Action.Result> results = action.invoke();
           Invocable.Action.Result result = results[0];
			               String str='Quote Creation Completed!!!';

           // Handle the response
           if (result.isSuccess()) {
               // Retrieve the Session id and Agent Response
               System.debug('Output Session Id: ' + result.getOutputParameters().get('sessionId'));
               action.setInvocationParameter('usermessage', 'Please create Quote for Ohana Technoligies Account with a Mobile with gaming usages');
                 results = action.invoke();
               action.setInvocationParameter('usermessage', 'Yes Please');
                 results = action.invoke();
                action.setInvocationParameter('usermessage', 'Use Account name as Acme for the Quote creation');
                 results = action.invoke();
                 action.setInvocationParameter('usermessage', 'Use Xiaomi as preferred Brand and create quote for me');
                 results = action.invoke();
               System.debug('Output Agent Response: ' + result.getOutputParameters().get('agentResponse'));
              

           } else {
               System.debug('Java action execution failed: ' + result.getErrors());
           }
           
            return(str);
       } catch (Exception e) {
           System.debug('Error invoking Java action: ' + e.getMessage());
                       return(e.getMessage());

       }
   }
}