const validateForm = (
    username: string,
    password: string
): string | undefined => {
    if (username.length === 0) {
        return "Username is required.";
    }
    if (password.length === 0) {
        return "Password is required.";
    }
    return undefined;
};

const validatePost = (text: string): boolean => text.length > 0;

export { validateForm, validatePost };
