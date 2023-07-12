import { Outlet, NavLink, Link } from "react-router-dom";

import gitlab from "../../assets/gitlab-icon.svg";
import { Logo } from "@dnb/eufemia";
import "@dnb/eufemia/style";

import styles from "./Layout.module.css";

const Layout = () => {
    return (
        <div className={styles.layout}>
            <header className={styles.header} role={"banner"}>
                <div className={styles.headerContainer}>
                    <Link to="/" className={styles.headerTitleContainer}>
                        <h3 className={styles.headerTitle}>GPT + DNB Insurance</h3>
                    </Link>
                    <nav>
                        <ul className={styles.headerNavList}>
                            <li>
                                <NavLink to="/" className={({ isActive }) => (isActive ? styles.headerNavPageLinkActive : styles.headerNavPageLink)}>
                                    Chat
                                </NavLink>
                            </li>
                            <li className={styles.headerNavLeftMargin}>
                                <NavLink to="/qa" className={({ isActive }) => (isActive ? styles.headerNavPageLinkActive : styles.headerNavPageLink)}>
                                    Ask a question
                                </NavLink>
                            </li>
                            <li className={styles.headerNavLeftMargin}>
                                <a href="https://gitlab.tech.dnb.no/dnb/platypus/tmt" target={"_blank"} title="GitLab repository link">
                                    <img
                                        src={gitlab}
                                        alt="GitLab logo"
                                        aria-label="Link to GitLab repository"
                                        width="25px"
                                        height="25px"
                                        className={styles.gitLabLogo}
                                    />
                                </a>
                            </li>
                        </ul>
                    </nav>
                    <h4 className={styles.headerRightText}>
                        <NavLink to="/about" className={({ isActive }) => (isActive ? styles.headerNavPageLinkActive : styles.headerNavPageLink)}>
                            Floyd the chatbot
                        </NavLink>
                    </h4>
                    <div className={styles.headerRightLogo}>
                        <a href="https://www.dnb.no/" target="_blank" title="DNB website">
                            <Logo style={{ color: "white", height: "30px" }} />
                        </a>
                    </div>
                </div>
            </header>

            <Outlet />
        </div>
    );
};

export default Layout;
