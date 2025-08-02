# -*- coding: utf-8 -*-

from argparse import Namespace


def tester_main(args: Namespace) -> None:
    assert isinstance(args.use_egl, bool)
    assert isinstance(args.use_glx, bool)
    assert isinstance(args.use_accelerate, bool)
    assert isinstance(args.no_accelerate, bool)

    if args.use_egl:
        assert not args.use_glx
        force_egl = True
    elif args.use_glx:
        assert not args.use_egl
        force_egl = False
    else:
        assert not args.use_glx
        assert not args.use_egl
        force_egl = None

    if args.use_accelerate:
        assert not args.no_accelerate
        use_accelerate = True
    elif args.no_accelerate:
        assert not args.use_accelerate
        use_accelerate = False
    else:
        assert not args.no_accelerate
        assert not args.use_accelerate
        use_accelerate = None

    from cvp.apps.tester.app import TesterApplication

    app = TesterApplication(force_egl, use_accelerate)
    app.start()
