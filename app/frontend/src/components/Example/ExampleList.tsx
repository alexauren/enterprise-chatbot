import { Example } from "./Example";

import styles from "./Example.module.css";

export type ExampleModel = {
    text: string;
    value: string;
};

const EXAMPLES: ExampleModel[] = [
    {
        text: "How much does insurance coverage typically cost?",
        value: "How much does insurance coverage typically cost?"
    },
    {
        text: "What types of events or damages are not covered by my insurance policy?",
        value: "What types of events or damages are not covered by my insurance policy?"
    },
    { text: "Can I transfer my insurance policy to a new vehicle or property?", value: "Can I transfer my insurance policy to a new vehicle or property?" }
];

interface Props {
    onExampleClicked: (value: string) => void;
}

export const ExampleList = ({ onExampleClicked }: Props) => {
    return (
        <ul className={styles.examplesNavList}>
            {EXAMPLES.map((x, i) => (
                <li key={i}>
                    <Example text={x.text} value={x.value} onClick={onExampleClicked} />
                </li>
            ))}
        </ul>
    );
};
