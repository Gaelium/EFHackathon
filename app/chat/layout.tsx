export const metadata = {
	title: "Doc chat",
	description: "AI Chat with the document",
};

export default function RootLayout({
	children,
}: {
	children: React.ReactNode;
}) {
	return <div>{children}</div>;
}
