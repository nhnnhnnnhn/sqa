"use client";

import FileView from "@/components/docview/FileView";
import { Suspense } from "react";
import { useSearchParams } from "next/navigation";
import styles from "./DocumentView.module.css";
import {API_URL} from "../../../../lib/service";

function DocumentPageContent() {
  const searchParams = useSearchParams();

  const linkParam = searchParams.get("link");
  const link = linkParam
    ? `${API_URL}/${linkParam}`
    : "";

  if (!link) {
    return <p>Không có tài liệu để hiển thị.</p>;
  }

  return (
    <div className={styles.pageWrapper}>
      <div className={styles.viewerContainer}>
        <FileView link={link} />
      </div>
    </div>
  );
}

export default function MyPage() {
  return (
    <Suspense fallback={<p>Dang tai tai lieu...</p>}>
      <DocumentPageContent />
    </Suspense>
  );
}
