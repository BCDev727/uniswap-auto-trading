const trader = artifacts.require("Trader");

module.exports = function (deployer) {
  deployer.deploy(trader);
};