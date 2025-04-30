public class CreateOpportunity {
    public void insertOpp() {
        // Create a new Opportunity object
        Opportunity opp = new Opportunity();

        // Set required and desired fields
        opp.Name = 'My New Opportunity'; // Required
        opp.StageName = 'Prospecting'; // Optional, but commonly used
        opp.CloseDate = Date.today().addDays(30); // Required
        opp.Amount = 1000.00; // Optional, but commonly used
        opp.AccountId = '001NS00001EPsENYA1'; // If you want to associate with an account

        // Insert the opportunity
        insert opp;
        createQuote(opp);
        System.debug(opp.Id);
        
    }
    public void createQuote( Opportunity opportunityIds) {
        Quote newQuote = new Quote();
        newQuote.OpportunityId = opportunityIds.Id; // Assuming only one Opportunity ID for simplicity
        newQuote.Name = 'Quote_' + System.now(); // Example name
        // Populate other fields as needed
        insert newQuote;
        System.debug(newQuote.Id);
    }
}