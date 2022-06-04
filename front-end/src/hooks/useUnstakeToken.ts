import { useEthers, useTokenBalance } from "@usedapp/core";
import networkMapping from "../chain-info/deployments/map.json";
import TokenFarm from "../chain-info/contracts/TokenFarm.json";
import { constants, utils } from "ethers";
import { Contract } from "@ethersproject/contracts";
import { useContractFunction } from "@usedapp/core";

export const useUnstakeToken = () => {
  const { chainId } = useEthers();

  console.log("chain id in unstakeToken hook is ", chainId);
  const tokenFarmAddress = chainId
    ? networkMapping[String(chainId)]["TokenFarm"][0]
    : constants.AddressZero;

  const { abi } = TokenFarm;
  const tokenFarmInterface = new utils.Interface(abi);

  const tokenFarmContract = new Contract(tokenFarmAddress, tokenFarmInterface);

  const { send: unstakeERC20, state: unstakeERC20State } = useContractFunction(
    tokenFarmContract,
    "unstakeTokens",
    { transactionName: "Unstake tokens" }
  );

  return { unstakeERC20, unstakeERC20State };
};
