# Profile Theory

## Purpose

This document defines what an Imprint profile is, what it is allowed to claim, and what it is forbidden from claiming.

## Core Principle

Imprint is an expression-analysis system.

It observes patterns.
It does not diagnose people.
It does not infer mental health conditions.
It does not infer intent.

## Subject -> Expression -> Voice

Imprint models:

Subject
  -> Expression
      -> Voice

The subject is the person, organization, or fictional public example being profiled.
Expression varies by context.
Voice is one manifestation of expression.

Imprint may use broad identity language in product prose, but schema-level contracts should not
claim to model identity, personality, values, or a mind. Schema fields should describe observable
expression patterns.

## Allowed Claims

Examples:

- Frequently uses operational evidence before generalization.
- Often begins explanations with a concrete example.
- Published writing is more formal than casual writing.
- Technical writing uses shorter paragraphs than conversational writing.
- Humor appears more frequently in informal communication.

These claims are supported by observable evidence.

## Forbidden Claims

Examples:

- The subject is depressed.
- The subject is bipolar.
- The subject is narcissistic.
- The subject has ADHD.
- The subject is anxious.
- The subject is an introvert.

These are interpretations or diagnoses.

Imprint must not generate them.

## Confidence Philosophy

Confidence applies to observations.

Confidence does not imply truth about a person.

Example:

Good:
"This pattern appeared in 82% of observed artifacts."

Bad:
"This person is analytical."

## Multi-Voice Principle

A subject may have multiple expression profiles.

Examples:

- casual
- technical
- published
- executive
- email
- podcast

Imprint should support a master profile plus derived profiles.

Derived profiles are explicit compiled context views. They should reference a baseline profile and
declare filters, divergences, and collisions rather than relying on hidden inheritance.
