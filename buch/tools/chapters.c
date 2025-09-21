/*
 * chapters.c
 *
 * (c) 2025 Prof Dr Andreas Müller
 */
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <getopt.h>
#include <regex.h>
#include <ctype.h>

int	debug = 0;

/**
 * \brief command line options
 */
static struct option options[] = {
{ "debug",	no_argument,		NULL,		'd' },
{ "auxfile",	required_argument,	NULL,		'a' },
{ "chapters",	no_argument,		NULL,		'c' },
{ "numbers",	no_argument,		NULL,		'n' },
{ "pages",	no_argument,		NULL,		'p' },
{ "help",	no_argument,		NULL,		'h' },
{ NULL,		0,			NULL,		 0  }
};

/* data structure for the chapter names, numbers and page numbers */
struct entry_s {
	char	*chapter;
	int	chapterno;
	int	page;
};
typedef struct entry_s	entry_t;
static entry_t	*entries = NULL;

/* flags */
int	pages = 0;
int	numbers = 0;

/* line counter for error messages */
int	linecounter;

/**
 * \brief help function
 *
 * \param progname
 */
static void	usage(char *progname) {
	printf("parse a LaTeX aux file for chapter page numbers and create\n");
	printf("a list of absolute page numbers from the input file, which\n");
	printf("can be standard input or the file specified on the comand\n");
	printf("line.\n\n");
	printf("usage:\n\n    %s [ options ] [ filename ]\n\n", progname);
	printf("options:\n\n");
	printf("  -a,--auxfile=<name>  name of the aux file <name> to use\n");
	printf("  -c,--chapters        dump chapter numbers\n");
	printf("  -d,--debug           show debug messages\n");
	printf("  -n,--numbers         show chapter numbers\n");
	printf("  -h,-?,--help         show this help message and exit\n");
	printf("  -p,--pages           display page numbers from aux file\n\n");
	printf("The --chapters option dumps the chapter info available at\n");
	printf("this point in the command line parsing process, so make\n");
	printf("sure the --auxfile option and any --numbers or --pages\n");
	printf("options apear before the --chapters option.\n\n");
}

/**
 * \brief Resize the array and add a new entry
 *
 * \param chapter	new chapter name
 * \param page		new page number
 */
static void	add_entry(char *chapter, int chapterno, int page) {
	if (debug) {
		fprintf(stderr, "%s:%d: add new entry\n", __FILE__, __LINE__);
	}
	/* count entries */
	int	counter = 0;
	entry_t	*p = entries;
	while (p->chapter) {
		counter++;
		p++;
	}
	if (debug) {
		fprintf(stderr, "%s:%d: %d entries present\n",
			__FILE__, __LINE__, counter);
	}
	entries = (entry_t *)realloc(entries, (counter + 2) * sizeof(entry_t));
	entries[counter].chapter = strdup(chapter);
	entries[counter].chapterno = chapterno;
	entries[counter].page = page;
	if (debug) {
		fprintf(stderr, "%s:%d: new entry '%s' -> %d added\n",
			__FILE__, __LINE__, chapter, page);
	}
	counter++;
	entries[counter].chapter = NULL;
	entries[counter].page = -1;
}

/**
 * \brief Find a chapter name
 *
 * \param chapter	chapter name to search for
 */
static int	find_chapter(const char *chapter) {
	entry_t	*p = entries;
	while (p->chapter) {
		if (0 == strcmp(p->chapter, chapter)) {
			return p->page;
		}
		p++;
	}
	return -1;
}

/**
 * \brief return the chapter from a number
 *
 * \param chapterno	chapter number to search for
 */
static int	find_chapterno(int chapterno) {
	entry_t	*p = entries;
	while (p->chapter) {
		if (p->chapterno == chapterno) {
			return p->page;
		}
		p++;
	}
	return -1;
}

/**
 * \brief Get number from the line
 *
 * \param line		the line to parse
 * \param m		the match to apply
 */
static int	get_number(const char *line, regmatch_t *m) {
	char	s[100];
	memset(s, 0, sizeof(s));
	strncpy(s, line + m->rm_so, (int)(m->rm_eo - m->rm_so));
	return atoi(s);
}

/**
 * \brief read aux file
 *
 * \param filename	read the file to get chapter names and numbers
 */
static int	build_entries(const char *filename) {
	/* initialize the entries array */
	entries = (entry_t *)malloc(sizeof(entry_t));
	entries->chapter = NULL;
	entries->page = -1;

	/* open an input file */
	FILE	*f = fopen(filename, "r");
	if (NULL == f) {
		fprintf(stderr, "cannot open file '%s': %s\n",
			filename, strerror(errno));
		return -1;
	}

	/* initialize the regular expression */
	char	*R = "\\newlabel{chapter:([a-z]*)}{{([0-9]+)}{([0-9]+)}.*";
	regex_t	r;
	int	rc = regcomp(&r, R, REG_EXTENDED | REG_ICASE);
	if (rc) {
		char	buf[1024];
		regerror(rc, &r, buf, sizeof(buf));
		fprintf(stderr, "cannot compile regex: %s\n", buf);
		return -1;
	}

	/* start reading the file */
	char	*line = NULL;
	size_t	l = 0;
	int	counter = 0;
	while (0 < (getline(&line, &l, f))) {
		regmatch_t	m[4];
		if (0 == regexec(&r, line, 4, m, 0)) {
			if (debug) {
				int	i;
				for (i = 0; i < 4; i++) {
					fprintf(stderr, "%s:%d: match %d %d\n", 
						__FILE__, __LINE__,
						(int)m[i].rm_so,
						(int)m[i].rm_eo);
				}
			}
			/* chapter */
			line[m[1].rm_eo] = '\0';
			char	*chapter = line + m[1].rm_so;
			/* chapterno */
			int	chapterno = get_number(line, m + 2);
			/* pageno */
			int	pageno = get_number(line, m + 3);
			/* debug */
			if (debug) {
				fprintf(stderr, "%s:%d: chapter='%s', "
					"page='%d', chapterno='%d'\n",
					__FILE__, __LINE__,
					chapter, pageno, chapterno);
			}
			/* add the entry */
			add_entry(chapter, chapterno, pageno);
			counter++;
		}
	}

	/* close the file */
	if (debug)
		fprintf(stderr, "%s:%d: closing file\n", __FILE__, __LINE__);
	fclose(f);

	/* destroy the regex */
	regfree(&r);

	/* return the number of entries */
	return counter;
}

/**
 * \brief get the information from a chapter line
 *
 * \param line		the line to parse
 */
static int	get_base(char *line) {
	/* check for chapter name */
	char	*e = strchr(line, '=');
	if (NULL == e) {
		fprintf(stderr, "cannot parse line '%s'\n",
			line);
		return -1;
	}
	e++;
	/* number or name */
	if (isdigit(*e)) {
		return find_chapterno(atoi(e));
	} else {
		return find_chapter(e);
	}
	fprintf(stderr, "chapter '%s' "
		"not found\n", e);
	return -1;
}

/**
 * \brief dump the chapter names
 */
void	dump_chapters() {
	entry_t	*p = entries;
	while (p->chapter) {
		printf("%s", p->chapter);
		if (numbers) {
			printf("[%d]", p->chapterno);
		}
		if (pages) {
			printf(" -> %d", p->page);
		}
		printf("\n");
		p++;
	}
}

/**
 * \brief main function
 *
 * \param argc
 * \param argv
 */
int	main(int argc, char *argv[]) {
	char	*filename = NULL;
	FILE	*file = stdin;

	/* parse command line */
	int	longindex;
	int	c;
	while (EOF != (c = getopt_long(argc, argv, "a:cdhnp", options,
			&longindex)))
		switch (c) {
		case 'a':
			if (build_entries(optarg) < 0) {
				fprintf(stderr, "cannot parse '%s'\n",
					optarg);
				return EXIT_FAILURE;
			}
			break;
		case 'c':
			dump_chapters();
			break;
		case 'd':
			debug = 1;
			break;
		case 'h':
			usage(argv[0]);
			return EXIT_SUCCESS;
		case 'n':
			numbers = 1;
			break;
		case 'p':
			pages = 1;
			break;
		}

	/* check for file name */
	if (optind < argc) {
		filename = argv[optind++];
		/* open the input file */
		file = fopen(filename, "r");
		if (NULL == file) {
			fprintf(stderr, "cannot open input file '%s': %s\n",
				filename, strerror(errno));
			return EXIT_FAILURE;
		}
		if (debug) {
			fprintf(stderr, "%s:%d: input file '%s'\n",
				__FILE__, __LINE__, filename);
		}
	}

	/* line counter for easier debug messages */
	linecounter = 0;

	/* parse read through the input file */
	char	*line = NULL;
	size_t	l = 0;
	int	base = -1;
	while (getline(&line, &l, file) > 0) {
		line[strlen(line)-1] = '\0';
		linecounter++;
		/* check contents of line */
		switch (line[0]) {
		case '#':
			/* skip comments */
			break;
		case 'c':
			/* chapter line, get chapter name/number and convert
			   to a page number */
			base = get_base(line);
			break;
		case '0':
		case '1':
		case '2':
		case '3':
		case '4':
		case '5':
		case '6':
		case '7':
		case '8':
		case '9':
			/* number line, contains relative page number, compute 
			   absolute page number */
			printf("%d,", base + atoi(line) - 1);
			break;
		default:
			/* ignore anything else */
			break;
		}
	}
	printf("\n");
	if (debug) {
		fprintf(stderr, "%s:%d: number of lines processed: %d\n",
			__FILE__, __LINE__, linecounter);
	}

	/* close the file */
	if (file != stdin)
		fclose(file);

	return EXIT_SUCCESS;
}
