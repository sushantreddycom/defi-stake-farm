import { useContractFunction, useEthers } from "@usedapp/core";
import TokenFarm from "../chain-info/contracts/TokenFarm.json";
import ERC20 from "../chain-info/contracts/MockERC20.json";
import networkMapping from "../chain-info/deployments/map.json";
import { constants, utils } from "ethers";
import { Contract } from "@ethersproject/contracts";
import { useEffect, useState } from "react";

// custom hook created to stake tokens
// pass the token address as input

export const useStakeTokens = (tokenAddress: string) => {
  // get the chain ID from useEthers
  const { chainId } = useEthers();

  const { abi } = TokenFarm;

  const tokenFarmAddress = chainId
    ? networkMapping[String(chainId)]["TokenFarm"][0]
    : constants.AddressZero;

  const tokenFarmInterface = new utils.Interface(abi);

  const tokenFarmContract = new Contract(tokenFarmAddress, tokenFarmInterface);

  const erc20ABI = ERC20.abi;
  const erc20Interface = new utils.Interface(erc20ABI);

  const erc20Contract = new Contract(tokenAddress, erc20Interface);

  const { send: approveErc20Send, state: approveErc20State } =
    useContractFunction(erc20Contract, "approve", {
      transactionName: "Approve ERC20 transfer",
    });

  const approveAndStake = (amount: string) => {
    setAmountToStake(amount);
    return approveErc20Send(tokenFarmAddress, amount);
  };

  const [isStateApproved, setisStateApproved] = useState(approveErc20State);

  // staking the amount, once approved
  const [amountToStake, setAmountToStake] = useState("0");
  const [trueState, setTrueState] = useState(approveErc20State);

  const { send: stakeErc20, state: stakeErc20State } = useContractFunction(
    tokenFarmContract,
    "stakeTokens",
    { transactionName: "Stake tokens" }
  );

  useEffect(() => {
    // only when state is approved
    if (isStateApproved) {
      stakeErc20(amountToStake, tokenAddress);
    }
  }, [isStateApproved, amountToStake, tokenAddress]);

  useEffect(() => {
    if (approveErc20State.status == "Success") {
      setTrueState(stakeErc20State);
    } else {
      setTrueState(approveErc20State);
    }
  }, [approveErc20State, stakeErc20State]);

  return { approveAndStake, trueState };
};
