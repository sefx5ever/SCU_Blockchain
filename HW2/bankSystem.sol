pragma solidity ^0.6.0;

contract bankSystem {
    mapping(string => address) public students;
    mapping(address => cdeatil) public balances;
    address payable owner;
    uint public capital;
    
    // Create client structure
    struct cdeatil {
        uint amount;
        bool isExist;
    }

    // To check account is enough money
    modifier isEnoughMoney(uint amount) {
        require(balances[msg.sender].amount > amount,"System Error: Account is not enoguh MONEY !");
        _;
    }
    
    // To check account is existing
    modifier isEnroll() {
        require(balances[msg.sender].isExist,"System Error: Account is not enroll, Please sign up !");
        _;
    }
    
    // Initianlize and assign owner
    constructor() public {
        owner = msg.sender;
    }
    
    // To deposit in bank account
    function deposit() public payable isEnroll {
        balances[msg.sender].amount+=msg.value;
        capital+=msg.value;
    }
    
    // To withdrawn from bank account
    function withdrawn(uint amount) public payable isEnoughMoney(amount) {
        balances[msg.sender].amount-=amount;
        capital-=amount;
    }
    
    // To transfer from acc to acc
    function transfer(uint amount,address payable adds) public payable isEnroll isEnoughMoney(amount) {
        if(balances[adds].isExist){
            balances[msg.sender].amount-=amount;
            balances[adds].amount+=amount;
        } else {
            revert("System Error: Account receiveable is no enroll !");
        }
    }
    
    // To get account latest balance
    function getBalance() public view isEnroll returns(uint) {
        return balances[msg.sender].amount;
    }
    
    // To show bank current balance
    function getBankBalance() external view returns(uint) {
        require(msg.sender == owner,"System Error: Sorry, you are not the bank owner !");
        return capital;
    }
    
    // To sign up acc
    function enroll(string memory stdId) public {
        if(balances[students[stdId]].isExist){
            revert("System Error: The student ID had been registered !");
        } else {
            students[stdId] = msg.sender;
            balances[msg.sender].amount = 0;
            balances[msg.sender].isExist = true;
        }
    }
    
    fallback() external {
        require(msg.sender == owner,"System Error: Permission Denied!");
        selfdestruct(owner);
    }
}
