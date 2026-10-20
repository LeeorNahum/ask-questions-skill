import { formatDate } from "../helpers/date";

export function ShareDialog({ url, createdAt }: { url: string; createdAt: Date }) {
  return (
    <dialog open>
      <h2>Share</h2>
      <input readOnly value={url} />
      <p>Created {formatDate(createdAt)}</p>
    </dialog>
  );
}
