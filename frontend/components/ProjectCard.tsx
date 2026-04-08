import Link from "next/link";

type ProjectCardProps = {
  id: string;
  title: string;
  domain: string;
  paperType: string;
  status: string;
};

export default function ProjectCard(props: ProjectCardProps) {
  return (
    <Link href={`/projects/${props.id}`} className="card">
      <div className="tag">{props.domain}</div>
      <h3>{props.title}</h3>
      <p className="muted">Type: {props.paperType}</p>
      <p className="muted">Status: {props.status}</p>
    </Link>
  );
}
