import { formatUnits } from "@ethersproject/units";
import { Button, Input, CircularProgress, Snackbar } from "@material-ui/core";
import { Alert } from "@material-ui/lab";
import { useEthers, useTokenBalance, useNotifications } from "@usedapp/core";
import { useStakeTokens } from "../../hooks/useStakeToken";
import { Token } from "../Main";
import React, { useEffect, useState } from "react";
import { utils } from "ethers";

export interface StakeFormProps {
  token: Token;
}

export const StakeForm = ({ token }: StakeFormProps) => {
  const { image, address, name } = token;
  const { account } = useEthers();
  const [amount, setAmount] = useState<number | string>(0);
  const tokenBalance = useTokenBalance(address, account);
  const { notifications } = useNotifications();

  const setStakeAmount = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newAmount =
      event.target.value === "" ? "" : Number(event.target.value);
    setAmount(newAmount);
  };
  const formattedTokenBalance: number = tokenBalance
    ? parseFloat(formatUnits(tokenBalance, 18))
    : 0;

  const { approveAndStake, trueState: stakeErc20State } =
    useStakeTokens(address);

  const approveAndStakeHandler = () => {
    const amountinWei = utils.parseEther(amount.toString());
    return approveAndStake(amountinWei.toString());
  };

  const isMining = stakeErc20State.status == "Mining";
  const [approveStatus, setApproveStatus] = useState(false);
  const [stakeStatus, setStakeStatus] = useState(false);

  const closeSnackHandler = () => {
    approveStatus && setApproveStatus(false);
    stakeStatus && setStakeStatus(false);
  };

  useEffect(() => {
    if (
      notifications.filter(
        (notification) =>
          notification.type == "transactionSucceed" &&
          notification.transactionName == "Approve ERC20 transfer"
      ).length > 0
    ) {
      setApproveStatus(true);
      setStakeStatus(false);
    }
    if (
      notifications.filter(
        (notification) =>
          notification.type == "transactionSucceed" &&
          notification.transactionName == "Stake tokens"
      ).length > 0
    ) {
      setStakeStatus(true);
    }
  }, [notifications]);

  return (
    <>
      <div>
        <Input onChange={setStakeAmount}></Input>
        <Button
          color="primary"
          size="large"
          onClick={approveAndStakeHandler}
          disabled={isMining}
        >
          {isMining ? <CircularProgress size={26} /> : "Stake"}
        </Button>
      </div>
      <Snackbar
        open={approveStatus}
        autoHideDuration={5000}
        onClose={closeSnackHandler}
      >
        <Alert onClose={closeSnackHandler} severity="success">
          ERC 20 transfer approved.{" "}
        </Alert>
      </Snackbar>
      <Snackbar
        open={stakeStatus}
        autoHideDuration={5000}
        onClose={closeSnackHandler}
      >
        <Alert onClose={closeSnackHandler} severity="success">
          Token staked.{" "}
        </Alert>
      </Snackbar>
    </>
  );
};
