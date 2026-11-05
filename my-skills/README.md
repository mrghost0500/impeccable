# My skills

Personal skill setup, kept apart from the impeccable product. Nothing in this folder is read by the
impeccable build.

- `website-design/` is the master skill. Ask for any website or UI work, or type
  `/website-design <what you want>`. It asks a few plain-language questions at the start, lets you
  choose between three looks, shows you a mockup in Figma to approve before building, shows you the
  real page before polishing it, and hands each stage to the right specialist skill. It can also
  build from a design you already have in Figma. Say "just build it" to skip the questions. To help
  pin down the feel, it can offer well-known sites as examples ("calm with lots of space, like
  Apple") from a library of 84 write-ups that the setup script downloads into
  `website-design/reference-sites/` from VoltAgent/awesome-design-md.
- `setup-skills.sh` installs the master skill and everything it calls into `~/.claude/skills`:
  impeccable, design-taste-frontend, ui-ux-pro-max, web-design-guidelines, webapp-testing,
  fixing-metadata, Claude SEO (26 skills and 19 helper agents), Emil Kowalski's 15 skills and 25 of
  Matt Pocock's. It sets impeccable, design-taste-frontend, ui-ux-pro-max and web-design-guidelines to
  start only by name or through `website-design`; run it with `ONLY_VIA_MASTER=0` to keep them
  starting on their own too.
- `REVIEW.md` is the review of the whole set that shaped the master skill: overlaps, clashes and
  gaps.

To get all of them in every new cloud session, put this in the environment's setup script:

```bash
git clone --depth 1 -q -b claude/impeccable-design-skill-u13s8t \
  https://github.com/mrghost0500/impeccable /tmp/my-skills \
  && bash /tmp/my-skills/my-skills/setup-skills.sh
rm -rf /tmp/my-skills
```

The first search-engine check needs a one-time `/seo setup`, which takes a few minutes.
