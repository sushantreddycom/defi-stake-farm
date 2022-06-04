import { Token } from "../Main";
import { useStakeBalance } from "../../hooks/useStakeBalance";
import { CircularProgress } from "@material-ui/core";
import { formatUnits } from "@ethersproject/units";

interface StakedBalanceProps {
  token: Token;
}

export const StakedBalance = ({ token }: StakedBalanceProps) => {
  const { image, address, name } = token;
  // const tokenFarmContract = utils.Interface(tokenFarmAddress, )
  const tokenBalance = useStakeBalance(address);

  const formattedTokenBalance = tokenBalance
    ? parseFloat(formatUnits(tokenBalance, 18))
    : 0;

  return (
    <>
      <div>Your current amount staked is {formattedTokenBalance}</div>
    </>
  );
};
