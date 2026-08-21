def emit(outcome: str, context: dict) -> None:
    """Print a single, canonical status message for the given outcome."""
    provider = context.get("provider", "")
    model = context.get("model", "")
    env_var = f"{provider.upper()}_API_KEY" if provider else "<PROVIDER>_API_KEY"
    next_cmd = f"python src/main.py --provider {provider} --model {model}"

    if outcome == "GENERATED":
        print(f"✓ Generated {provider} adapter.")
        print(f"Set {env_var}=... in .env, then run: {next_cmd}")
    elif outcome == "PROVIDER_EXISTS":
        print(f"Provider `{provider}` already supported.")
        print(f"Run: {next_cmd}")
    elif outcome == "AMBIGUOUS":
        closest = context.get("closest_match")
        given_model = context.get("model", "")
        if closest:
            print(f"Could not resolve model. Did you mean `{closest}`?")
        else:
            print(f"Could not resolve model `{given_model}` — provider unknown or model unclear.")
    else:
        print(f"Unknown outcome: {outcome}")
