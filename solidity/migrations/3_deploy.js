let Voting = artifacts.require("./Voting.sol");
let Ranking = artifacts.require("./Ranking.sol");
let Faucet = artifacts.require("./Faucet.sol");
let Admin = artifacts.require("./Admin.sol");
let Token = artifacts.require("./Token.sol");

// dynamicFeeLinearRate, dynamicFeeLinearPrecision, maxOverStakeFactor,
// maxFixedFeeRate, maxFixedFeePrecision, unstakeSpeed,
// currentCommitTtl, currentRevealTtl, initialAvgStake
let rankingParams = [ 1, 100, 100, 1, 10, web3.toWei(0.05), 30, 30, web3.toWei(300) ];
let totalSupply = web3.toWei(1000000);
let faucetRate = 3600;
let faucetSize = web3.toWei(1000);

module.exports = async function(deployer, network, accounts) {
    let voting, ranking, faucet, admin, token;

    deployer.then(function() {
        return Voting.new();
    }).then(function(instance) {
        voting = instance;
        console.log('Voting:', voting.address);

        return Admin.new();
    }).then(function(instance) {
        admin = instance;
        console.log('Admin:', voting.address);

        return Token.new();
    }).then(function(instance) {
        token = instance;
        console.log('Token:', admin.address);

        return Ranking.new(admin.address);
    }).then(function(instance) {
        ranking = instance;
        console.log('Ranking:', ranking.address);

        return Faucet.new(admin.address);
    }).then(function(instance) {
        faucet = instance;
        console.log('Faucet:', faucet.address);

        return ranking.init(voting.address, token.address, ...rankingParams);
    }).then(async function () {
        console.log('Ranking inited');

        return faucet.init(ranking.address);
    }).then(async function () {
        console.log('Faucet inited');

        return faucet.setFaucetRate(faucetRate);
    }).then(async function () {
        console.log('Faucet rate');

        return faucet.setFaucetSize(faucetSize);
    }).then(async function () {
        console.log('Faucet size');

        return token.transfer(faucet.address, totalSupply);
    }).then(async function () {
        console.log('Faucet charged');
    })
    .catch(e => console.log(e));

};
