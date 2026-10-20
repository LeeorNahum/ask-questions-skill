import { formatMoney } from "../helpers/money";

export function Pricing() {
  return <p>Pro: {formatMoney(900)} per month</p>;
}
