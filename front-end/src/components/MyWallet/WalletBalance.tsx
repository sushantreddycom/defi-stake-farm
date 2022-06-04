import React from "react";
import { useEthers, useTokenBalance } from "@usedapp/core";
import { Token } from "../Main";
import { formatUnits } from "@ethersproject/units";
import { BalanceMsg } from "./BalanceMsg";

interface WalletBalanceProps {
  token: Token;
}

export const WalletBalance = ({ token }: WalletBalanceProps) => {
  const { image, address, name } = token;
  const { account } = useEthers();
  console.log("Address of token", address);
  console.log("Address of account", account);
  const tokenBalance = useTokenBalance(address, account);
  console.log("token balance", tokenBalance);
  const formattedTokenBalance: number = tokenBalance
    ? parseFloat(formatUnits(tokenBalance, 18))
    : 0;

  return (
    <BalanceMsg
      img={image}
      name={name}
      balance={formattedTokenBalance}
    ></BalanceMsg>
  );
};
